import asyncio


from config import *
from manga_list import MangaList
from farmChapters import *
from farmComments import *
from farmDailyLightnings import *


def main():
    manga = MangaList()
    async def farm():
        result = await asyncio.gather(
            farmComments(),
            farmChapters(manga),
            farmDailyLightning()
        )
        print(f'\nИтого нафармлено молний: {sum(result)}')
    asyncio.run(farm())
    manga.saveMangaList()


if __name__ == '__main__':
    main()