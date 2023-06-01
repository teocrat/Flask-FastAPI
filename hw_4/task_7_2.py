from random import randint
from multiprocessing import Process
import time

COUNT = 1000000
START = 1
STOP = 100
TIMES = 5


def sum_large_list() -> None:
    lst = [randint(START, STOP) for _ in range(COUNT)]
    print(sum(lst))
    print(f"Completed in {time.time() - start_time:.2f} seconds")


processes = []

start_time = time.time()

if __name__ == '__main__':
    for i in range(TIMES):
        process = Process(target=sum_large_list)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
