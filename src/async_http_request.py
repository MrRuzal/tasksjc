"""
Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов
и возвращает словарь, где ключами являются URL, а значениями — статус-коды ответов.
Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:

Ограничьте количество одновременных запросов до 5
(используйте примитивы синхронизации из asyncio библиотеки)
Обработайте возможные исключения (например, таймауты, недоступные ресурсы)
и присвойте соответствующие статус-коды (например, 0 для ошибок соединения).
Сохраните все результаты в файл
"""

import asyncio
import json

import aiohttp


async def fetch(
    session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore
) -> dict:
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                return {"url": url, "status_code": response.status}
        except Exception:
            return {"url": url, "status_code": 0}


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

    with open(file_path, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url",
    ]

    asyncio.run(fetch_urls(urls, "src/results.json"))
