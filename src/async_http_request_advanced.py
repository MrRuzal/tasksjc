"""
 Асинхронный HTTP-запрос. Продвинутая реализация.
Напишите асинхронную функцию fetch_urls, которая принимает файл со списком урлов
(каждый URL адрес возвращает JSON) и сохраняет результаты выполнения в другой файл
 (result.jsonl), где ключами являются URL, а значениями — распарсенный json,
 при условии что статус код — 200. Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:

Ограничьте количество одновременных запросов до 5
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) ошибок соединения
Контекст:

Урлов в файле может быть десятки тысяч
Некоторые урлы могут весить до 300-500 мегабайт
При внезапной остановке и/или перезапуске скрипта - допустимо скачивание урлов по новой.
Пример файла results.json:

{"url": "https://example1.com", "content": {"any key": "any value}
{"url": "https://example2.com", "content": {"key": "value", ...}
"""

import asyncio
import json

import aiohttp
from aiofiles import open as aio_open

MAX_CONCURRENT_REQUESTS = 5


async def fetch_url(
    session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore
):
    async with semaphore:
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                if response.status == 200:
                    try:
                        text = await response.text()
                        content = json.loads(text)
                        return {"url": url, "content": content}
                    except Exception:
                        return None
                else:
                    return None
        except Exception:
            return None


async def fetch_urls(input_file: str, output_file: str):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with (
        aio_open(input_file, "r") as infile,
        aio_open(output_file, "w") as outfile,
    ):
        async with aiohttp.ClientSession() as session:
            tasks = []
            async for line in infile:
                url = line.strip()
                if not url:
                    continue
                tasks.append(fetch_url(session, url, semaphore))

                if len(tasks) >= 100:
                    results = await asyncio.gather(*tasks)
                    for result in results:
                        if result:
                            await outfile.write(
                                json.dumps(result, ensure_ascii=False) + "\n"
                            )
                    tasks.clear()

            if tasks:
                results = await asyncio.gather(*tasks)
                for result in results:
                    if result:
                        await outfile.write(
                            json.dumps(result, ensure_ascii=False) + "\n"
                        )


if __name__ == "__main__":
    asyncio.run(fetch_urls("src/urls.txt", "src/results.json"))
