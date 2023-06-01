import asyncio
import aiohttp
import time
import sys

urls = ['https://i.pinimg.com/736x/21/84/93/218493cd9eaec681966af6b87ca95195--emoji-emoticons-smileys.jpg',
        'https://klike.net/uploads/posts/2023-02/1675518503_3-45.jpg',
        'https://papik.pro/uploads/posts/2023-02/1675861539_papik-pro-p-nosov-zateiniki-risunok-2.jpg',
        'https://papik.pro/uploads/posts/2021-10/1634719816_28-papik-pro-p-otkritki-smailiki-28.jpg',
        'https://uroki-risovanie.ru/wp-content/uploads/2022/11/vlyublennyy-smayl1.jpg',
        'https://papik.pro/uploads/posts/2023-02/1675861541_papik-pro-p-nosov-zateiniki-risunok-7.jpg',
        'https://papik.pro/uploads/posts/2021-10/1634719797_18-papik-pro-p-otkritki-smailiki-18.jpg'
        ]

# urls = sys.argv[1:]


async def download(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()
                filename = url.rstrip('/').split("/")[-1]
                with open(filename, "wb") as f:
                    f.write(content)
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
