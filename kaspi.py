import os

import aiohttp
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('KASPI_TOKEN')

async def get_info_for_order(kaspi_order_num):
    headers = {
        "X-Auth-Token": str(TOKEN)
    }

    url = f"https://kaspi.kz/shop/api/v2/orders?filter[orders][code]={int(kaspi_order_num)}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print("Status:", response.status)

            if response.status == 200:
                data = await response.json()
                return data
            else:
                text = await response.text()
                print("Ошибка:", text)
                return None
