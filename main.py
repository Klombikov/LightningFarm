import asyncio


from config import *
from manga_list import MangaList
from farmLightnings import *
from schemas import *


def checkEnvFile():
    """Функция, проверяющая наличие .env файла."""
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv('AUTORIZATION'):
        raise FileNotFoundError("Не найден файл \".env\".")
    

class CLIOutput():
    """Класс, отвечающий за вывод информации

    Данный класс нужен для того, чтобы в консоли выводилась информация о карточках и молниях
    таким образом, чтобы молнии были всегда внизу.
    """
    def __init__(self):
        """Инициализация класса"""
        self._outputTextLength = 128
        self.coins = 0
        self._printCoins()


    def _printCoins(self):
        """Функция, которая выводит количество молний."""
        text = f"Нафармлено молний: {self.coins}"
        text += " " * (self._outputTextLength - len(text))
        self.coinsTextOutput = text
        print(self.coinsTextOutput, end='\r')


    def sendMessage(self, text):
        print(text)
        print()


    def sendRewards(self, rewardsResult: RewardsResult):
        """Функция, которая выводит информацию о нафармленном.

        Parameters:
            rewardsResult (RewardsResult):
                Словарь, в котором содержатся награды.
        """
        if rewardsResult["card"]:
            text = f"Вам выпала карта {rewardsResult['card']['rank']} ранга"
            text += " " * (self._outputTextLength - len(text))
            print(text)
            print(self.coinsTextOutput, end='\r')
        if rewardsResult["coins"]:
            self.coins += rewardsResult["coins"]
            self._printCoins()


    def end(self):
        print(self.coinsTextOutput)


def main():
    try:
        checkEnvFile()
        manga = MangaList()
        callback = CLIOutput()
        lightningFarm = LightningFarm(manga, callback.sendRewards)
        asyncio.run(lightningFarm.startFarm())
        manga.saveMangaList()
        callback.end()
    except Exception as e:
        print('Что-то пошло не так, программа аварийно закрылась. Ошибка:\n', e)


if __name__ == '__main__':
    main()