import aiohttp
from config import *
import asyncio


from manga_list import MangaList
from schemas import *


class LightningFarm():
    """Ферма молний."""
    def __init__(self, mangaList: MangaList, callback=lambda *args, **kwargs: None) -> None:
        """Инициализация класса.

        Args:
            mangaList: список манги
            def: функция, в которую будут передаваться нафармленные молнии и карточки
        """
        self.mangaList = mangaList
        self.callback=callback
    

    async def _readChapter(self, chapterId: int) -> dict:
        """Чтение одной главы

        Args:
            chapterId (int): 
                ID главы, которую надо прочесть

        Returns:
            RewardsResult: 
                Пустой список, либо список с наградами за чтение (молнии или карта)
        """
        postResponse = None
        async with aiohttp.ClientSession() as session:
            async with session.post(readChapterUrl, headers=headers, json={"page": 1, "chapter": chapterId}) as response:
                postResponse = response
                if postResponse.status == 200:
                    return await postResponse.json()
                # Вставить обработку ошибки соединения
                # Вставить обработку результата
                else:
                    return []
                
    
    async def _getChaptersFromPage(self, branch_id, page=1):
        """Поиск глав

        Args:
            branch_id: branch_id манги
            page: страница поиска глав

        Returns:
            Список глав и следующая страница
        """
        chapters = []
        data = None
        async with aiohttp.ClientSession() as session:
            async with session.get(chaptersUrl + f"&ordering=index&branch_id={branch_id}&page={page}", headers=headers) as response:
                data = await response.json()
        if "results" not in data.keys():
            return chapters, None
        
        for i in range(len(data["results"])):
            chapter: Chapter = {
                "id": data["results"][i]["id"],
                "chapter": data["results"][i]["chapter"],
                "is_paid": data["results"][i]["is_paid"],
                "is_bought": data["results"][i]["is_bought"],
                "viewed": data["results"][i]["viewed"]
            }
            chapters.append(chapter)
        if "next" not in data.keys() or not data["next"]:
            return chapters, None
        return chapters, data["next"]
                
    
    async def _findUnreadedChapters(self):
        """Нахождение непрочитанных глав

        Args:
            список манги

        Returns:
            Список непрочитанных глав
        """
        unreadedChapters = []
        while True:
            if not self.mangaList.getCurrentBranchId:
                return []
            chapters, nextPage = await self._getChaptersFromPage(self.mangaList.getCurrentBranchId(), self.mangaList.getCurrentPage())
            if chapters == []:
                return []
            for chapter in chapters:
                if chapter["viewed"] != True and chapter["is_paid"] == False:
                    unreadedChapters.append(chapter)
            if unreadedChapters:
                return unreadedChapters
            elif nextPage:
                self.mangaList.changeCurrentPage(nextPage)
            else: 
                self.mangaList.chooseNextManga()
                
    
    async def _getLightningForReading(self, maxReadedChapters=10):
        """Получение молний за чтение

        Args:
            maxReadedChapters (int, optional): 
                максимальное количество глав, которые будут фармиться до получения молний

        Returns:
            int:
                Полученные молнии за чтение
        """
        iteration = 0
        lightning = 0
        flag = False
        while True:
            chapters = await self._findUnreadedChapters()
            for chapter in chapters:
                iteration += 1
                response = await self._readChapter(chapter["id"])
                await asyncio.sleep(0.5)
                if response and "rewards" in response.keys():
                    lightning += self._processRewards(response["rewards"])
                if lightning:
                    return lightning
                if iteration > maxReadedChapters:
                    flag = True
                    break
            if flag: break
        return lightning
                

    async def _farmChapters(self, maxReadCount=41) -> None:
        """Фарм молний за чтение

        Данная функция читает главы и собирает награды за это.

        Args:
            maxReadCount (int, optional): сколько наград в виде молний будем собирать

        Returns:
            int:
                Количество нафармленных молний
        """
        for _ in range(maxReadCount):
            if await self._getLightningForReading() == 0:
                break
                

    async def _farmComments(self, maxCommentsCount=21) -> None:
        """Фарм молний за комментирование.

        Данная функция пишет комментарии на реманге и собирает награды за это.

        Args:
            maxCommentsCount (int, optional): максимальное количество комментариев, которое будет фармиться.
        """
        for i in range(maxCommentsCount):
            postResponse = None
            async with aiohttp.ClientSession() as session:
                async with session.post(commentUrl, headers=headers, json=commentChapterPayload) as response:
                    if response.status == 200:
                        postResponse = await response.json()
                    # postResponse = await response.json()
                    # Сюда добавить отработку ошибки при потере соединения
            await asyncio.sleep(4)

            async with aiohttp.ClientSession() as session:
                async with session.delete(commentUrl + str(postResponse['id']), headers=headers) as response:
                    # Сюда добавить отработку ошибки при потере соединения
                    ...

            if postResponse and 'rewards' in postResponse.keys() and postResponse['rewards']:
                self._processRewards(postResponse['rewards'])
            else:
                break
            await asyncio.sleep(60)


    async def _farmDailyLightning(self) -> None:
        """Фарм молний за ежедневный вход.

        Данная функция отправляет запрос на ремангу для сбора ежедневной награды.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(currentUserUrl, headers=headers) as response:
                result = await response.json()
                if "rewards" in result.keys():
                    # Добавить обработку ошибок, когда реманга не отвечает
                    self._processRewards(result["rewards"])


    def _processRewards(self, rewards) -> int:
        """
        Обработка наград.

        Данная функция обрабатывает награды, получаемые за чтение главы или написание комментария.

        Parameters:
            response:
                Ответ от запроса на ремангу, которые могут вернуть награду

        Returns:
            int: 
                Количество выданных молний
        """
        result: RewardsResult = {
            "card": None,
            "coins": 0
        }
        for item in rewards:
            if item["type"] == "coins":
                result["coins"] += int(item["value"])
            elif item["type"] == "card":
                card: CardData = {
                    "id": item["value"]["id"],
                    "rank": str(item["value"]["rank"][-1]).upper(),
                    "imgUrl": item["value"]["cover"]["mid"]
                }
                result["card"] = card
            else:
                ...
        self.callback(result)
        return result["coins"]

    
    async def startFarm(self) -> int:
        """Начать фарм молний.

        Returns:
            int:
                Количество нафармленных молний.
        """
        tasks = [
            asyncio.create_task(self._farmChapters()),
            asyncio.create_task(self._farmComments()),
            asyncio.create_task(self._farmDailyLightning())
        ]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)