import json

import httpx
import asyncio


async def fetch(url, session):
    try:
        response = await session.post(
            url,
            data=json.dumps({
                "password": "root",
                "email": "root@example.com",
            }),
            headers={"Content-Type": "application/json"},
        )
        return response.status_code

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None


async def fetch_all(urls):
    async with httpx.AsyncClient() as session:
        tasks = [fetch(url, session) for url in urls]
        return await asyncio.gather(*tasks)


async def main():
    while True:
        urls = [
            "http://0.0.0.0:8000/auth/obtain-token" for _ in range(2000)
        ]
        responses = await fetch_all(urls)
        print(responses)


asyncio.run(main())
