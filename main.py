import asyncio

from config import *
from manga_list import MangaList
from farmChapters import *
from farmComments import *


def main():
    sumLightning = 0
    sumCards = 0
    
    manga = MangaList()
    async def farm():
        result = await asyncio.gather(
            #farmComments()
            farmChapters(manga)
        )
        print(result)
    asyncio.run(farm())
    print(f'\nИтого нафармлено молний: {sumLightning}')
    print(f'Выпало карточек: {sumCards}')
    manga.saveMangaList()

if __name__ == '__main__':
    main()
