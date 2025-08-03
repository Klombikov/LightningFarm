import aiohttp
import asyncio


from processRewards import *
from config import *


async def farmComments(maxCommentsCount=21):
    lightning = 0
    for i in range(maxCommentsCount):
        postResponse = None
        async with aiohttp.ClientSession() as session:
            async with session.post(commentUrl, headers=headers, json=commentChapterPayload) as response:
                postResponse = await response.json()
        await asyncio.sleep(4)

        async with aiohttp.ClientSession() as session:
            async with session.delete(commentUrl + str(postResponse['id']), headers=headers) as response:
                ...

        if 'rewards' in postResponse.keys() and postResponse['rewards']:
            lightning += processRewards(postResponse['rewards'])
        
        else:
            print('Молний за комменты больше не дают')
            break
        await asyncio.sleep(60)
    return lightning