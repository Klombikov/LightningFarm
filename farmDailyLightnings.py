import aiohttp


from config import *
from processRewards import *


async def farmDailyLightning():
    async with aiohttp.ClientSession() as session:
        async with session.get(currentUserUrl, headers=headers) as response:
            result = await response.json()
            if "rewards" in result.keys():
                lightning = 0
                lightning += processRewards(result["rewards"])
                return lightning
    return 0