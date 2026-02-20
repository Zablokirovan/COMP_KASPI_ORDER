# kaspi.py
import os
import aiohttp
import asyncio
import socket
from dotenv import load_dotenv

load_dotenv()
#kaspi token
TOKEN = os.getenv("KASPI_TOKEN")

TIMEOUT = aiohttp.ClientTimeout(total=120, connect=10, sock_read=90)

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


async def sending_code(order_id, text, session: aiohttp.ClientSession,security_code: str | None = None):
    url = "https://kaspi.kz/shop/api/v2/orders"
    headers = {"X-Send-Code": "true",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json;charset=UTF-8",   # можно оставить, у тебя уже работало
        "X-Auth-Token": str(TOKEN),
        "X-Security-Code": "" if security_code is None else str(security_code),}
    payload = {
        "data": {
            "type": "orders",
            "id": order_id,
            # ВАЖНО: это ordersID (id из ответа Kaspi), НЕ code
            "attributes": {
                "code": str(text),  # это номер заказа (code)
                "status": "COMPLETED",
            },
        }
    }
    try:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status != 200:
                err = await resp.text()
                print("Kaspi HTTP", resp.status, err[:500])
                return None
            return await resp.json(content_type=None)

    except asyncio.TimeoutError:
        print("Kaspi timeout")
        return None
    except aiohttp.ClientError as e:
        print("Kaspi client error:", repr(e))
        return None

