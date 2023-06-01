import asyncio
import aiohttp
import time

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://www.codewars.com/',
        'https://proglib.io/p/python-i-mysql-prakticheskoe-vvedenie-2021-01-06',
        'https://www.rambler.ru/',
        'https://stepik.org/catalog',
        'https://pythonist.ru/svyaznyj-spisok-na-python-chto-eto-takoe-i-kak-ego-realizovat/'
        ]


async def download(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                filename = 'a_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(text)
                    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")
    except Exception:
        print('Check URL')


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
