import aiohttp


from config import *

async def farmDailyLightning():
    async with aiohttp.ClientSession() as session:
        async with session.get(currentUserUrl, headers=headers) as response:
            print(response.status)
            print(await response.json())
            if "rewards" in response.json():
                print(response.json()["rewards"])
                return response.json()["rewards"]
    return None