from random import randint
import threading
import time

COUNT = 1000000
START = 1
STOP = 100
TIMES = 5


def sum_large_list() -> None:
    lst = [randint(START, STOP) for _ in range(COUNT)]
    print(sum(lst))
    print(f"Completed in {time.time() - start_time:.2f} seconds")


threads = []

start_time = time.time()

if __name__ == '__main__':
    for i in range(TIMES):
        thread = threading.Thread(target=sum_large_list)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
