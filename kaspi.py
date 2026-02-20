# kaspi.py
import os
import aiohttp
import asyncio
import socket
from dotenv import load_dotenv

load_dotenv()
#kaspi token
TOKEN = os.getenv("KASPI_TOKEN")

TIMEOUT = aiohttp.ClientTimeout(total=30, connect=7, sock_read=25)

def make_session():
    connector = aiohttp.TCPConnector(
        family=socket.AF_INET,
        ttl_dns_cache=300,
        limit=20,
    )
    return aiohttp.ClientSession(timeout=TIMEOUT, connector=connector)

async def get_info_for_order(session: aiohttp.ClientSession, kaspi_order_num: str | int):
    url = "https://kaspi.kz/shop/api/v2/orders"
    params = {"filter[orders][code]": str(int(kaspi_order_num))}

    headers = {
        "X-Auth-Token": TOKEN,
        "Accept": "application/vnd.api+json;charset=UTF-8",
        # иногда полезно, но не обязательно:
        "User-Agent": "Mozilla/5.0",
    }

    try:
        async with session.get(url, headers=headers, params=params) as resp:
            text = await resp.text()

            if resp.status != 200:
                print("Kaspi HTTP", resp.status, text[:500])
                return None

            # JSON:API обычно с правильным content-type, но оставим страховку
            return await resp.json(content_type=None)

    except asyncio.TimeoutError:
        print("Kaspi timeout")
        return None
    except aiohttp.ClientError as e:
        print("Kaspi client error:", repr(e))
        return None