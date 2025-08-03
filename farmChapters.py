import aiohttp
from config import *
import asyncio


from manga_list import MangaList
from processRewards import *


async def getChaptersFromPage(branch_id, page=1):
    chapters = []
    data = None
    async with aiohttp.ClientSession() as session:
        async with session.get(chaptersUrl + f"&ordering=index&branch_id={branch_id}&page={page}", headers=headers) as response:
            data = await response.json()
    if "results" not in data.keys():
        return chapters, None
    
    for i in range(len(data["results"])):
        chapters.append({
            "id": data["results"][i]["id"],
            "chapter": data["results"][i]["chapter"],
            "is_paid": data["results"][i]["is_paid"],
            "is_bought": data["results"][i]["is_bought"],
            "viewed": data["results"][i]["viewed"]
        })
    if "next" not in data.keys() or not data["next"]:
        return chapters, None
    return chapters, data["next"]


async def getAllMangaChapters(branch_id):
    chapterList = []
    currentPage = 1
    while True:
        newChapters, nextPage = await getChaptersFromPage(branch_id, currentPage)
        chapterList = chapterList + newChapters
        if not nextPage: break
        else: currentPage = nextPage
    return chapterList


async def readChapter(chapterId):
    postResponse = None
    async with aiohttp.ClientSession() as session:
        async with session.post(readChapterUrl, headers=headers, json={"page": 1, "chapter": chapterId}) as response:
            postResponse = response
            if postResponse.status == 200:
                return await postResponse.json()
            else:
                return []


async def findUnreadedChapters(mangaList: MangaList):
    unreadedChapters = []
    while True:
        if not mangaList.getCurrentBranchId:
            return []
        chapters, nextPage = await getChaptersFromPage(mangaList.getCurrentBranchId(), mangaList.getCurrentPage())
        if chapters == []:
            return []
        for chapter in chapters:
            if chapter["viewed"] != True and chapter["is_paid"] == False:
                unreadedChapters.append(chapter)
        if unreadedChapters:
            return unreadedChapters
        elif nextPage:
            mangaList.changeCurrentPage(nextPage)
        else: 
            mangaList.chooseNextManga()


async def getLightningForReading(mangaList: MangaList, maxReadedChapters=10):
    iteration = 0
    lightning = 0
    flag = False
    while True:
        chapters = await findUnreadedChapters(mangaList)
        for chapter in chapters:
            iteration += 1
            response = await readChapter(chapter["id"])
            await asyncio.sleep(0.5)
            if response and "rewards" in response.keys():
                lightning += processRewards(response["rewards"])
            if iteration > maxReadedChapters:
                flag = True
                break
            if lightning:
                return lightning
        if flag: break
    return lightning


async def farmChapters(mangaList: MangaList, maxCommentsCount=41):
    sumLightning = 0
    try:
        iteration = 0
        while True:
            lightning = await getLightningForReading(mangaList)
            if lightning == 0 or iteration > maxCommentsCount:
                break
            sumLightning += lightning
            iteration += 1
        return sumLightning
    except Exception as e:
        print(f"Возникла ошибка при фарме молний за чтение:\n{e}")
        return sumLightning