import os


from jsonLoader import jsonLoader
from getMangaBranchId import getMangaBranchId


class MangaList():
    """Класс, отвечающий за хранение манги.
    
    Данный класс загружает, обрабатывает и сохраняет список читаемой манги.
    """
    _mangaList = None
    _readingListPath = None


    def __init__(
            self,
            readingListPath="./data/reading_list.json"
    ):
        """Инициализация класса

        Parameters:
            readingListPath (Path):
                Путь к файлу, в котором хранится список манги.
        """
        self._readingListPath = readingListPath
        if not os.path.exists(self._readingListPath):
            self.downloadMangaList()
        else:
            self._mangaList = jsonLoader.LoadFile(self._readingListPath)


    def downloadMangaList(self) -> None:
        """Функция, загружающая список манги.

        Функция, которая загружает новый список манги.
        """
        self._mangaList = getMangaBranchId(targetURLCount=1000)
        self._mangaList["current"] = self._mangaList["in_queue"].pop(0)
        self.saveMangaList()


    def saveMangaList(self) -> None:
        """Функция, сохраняющая список манги в файл."""
        jsonLoader.SaveFile(self._readingListPath, self._mangaList)


    def chooseNextManga(self) -> None:
        """Выбор следующей по списку манги."""
        self._mangaList["finished"].append(self._mangaList["current"])
        if self._mangaList["in_queue"]:
            self._mangaList["current"] = self._mangaList["in_queue"].pop(0)
        else:
            self._mangaList["current"] = None
        self.saveMangaList()


    def getCurrentBranchId(self):
        """Получить branch_id текущей манги."""
        return self._mangaList["current"]["branch_id"]


    def getCurrentPage(self):
        """Получить страницу манги, на которой остановились."""
        return self._mangaList["current"]["current_page"]


    def changeCurrentPage(self, newPage):
        """Изменить текущую страницу манги.
        
        Parameters:
            newPage (int):
                Страница, которую хотим сделать текущей.
        """
        self._mangaList["current"]["current_page"] = newPage

