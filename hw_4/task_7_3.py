from random import randint
import asyncio
import time

COUNT = 1000000
START = 1
STOP = 100
TIMES = 5


async def sum_large_list() -> None:
    lst = [randint(START, STOP) for _ in range(COUNT)]
    print(sum(lst))
    print(f"Completed in {time.time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for i in range(TIMES):
        task = asyncio.ensure_future(sum_large_list())
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
