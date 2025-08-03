import os


from jsonLoader import jsonLoader
from getMangaBranchId import getMangaBranchId


class MangaList():

    _mangaList = None
    _readingListPath = None

    def __init__(
            self,
            readingListPath="./data/reading_list.json"
    ):
        self._readingListPath = readingListPath
        if not os.path.exists(self._readingListPath):
            self.updateMangaList()
        else:
            self._mangaList = jsonLoader.LoadFile(self._readingListPath)

    def updateMangaList(self):
        self._mangaList = getMangaBranchId(targetURLCount=30)
        self._mangaList["current"] = self._mangaList["in_queue"].pop(0)
        self.saveMangaList()

    def saveMangaList(self):
        jsonLoader.SaveFile(self._readingListPath, self._mangaList)

    def chooseNextManga(self):
        self._mangaList["finished"].append(self._mangaList["current"])
        if self._mangaList["in_queue"]:
            self._mangaList["current"] = self._mangaList["in_queue"].pop(0)
        else:
            self._mangaList["current"] = None
        self.saveMangaList()

    def getCurrentBranchId(self):
        return self._mangaList["current"]["branch_id"]

    def getCurrentPage(self):
        return self._mangaList["current"]["current_page"]

    def changeCurrentPage(self, newPage):
        self._mangaList["current"]["current_page"] = newPage

