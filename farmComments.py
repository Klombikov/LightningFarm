import aiohttp
from config import *
import asyncio


async def farmComments():
    rewards = []
    for i in range(MAX_COUNT_COMMENTS):
        postResponse = None
        async with aiohttp.ClientSession() as session:
            async with session.post(commentUrl, headers=headers, json=commentChapterPayload) as response:
                postResponse = await response.json()
        await asyncio.sleep(4)

        async with aiohttp.ClientSession() as session:
            async with session.delete(commentUrl + str(postResponse['id']), headers=headers) as response:
                ...

        if 'rewards' in postResponse.keys() and postResponse['rewards']:
            rewards.append(postResponse['rewards'])
        
        else:
            print('Молний за комменты больше не дают')
            break
        await asyncio.sleep(60)
    return rewards