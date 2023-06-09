import requests
from multiprocessing import Process
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


def download(url):
    try:
        response = requests.get(url)
        filename = 'p_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'

        with open(filename, "w", encoding='utf-8') as f:
            f.write(response.text)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")
    except Exception:
        print('Check URL')


processes = []
start_time = time.time()
if __name__ == '__main__':
    for url in urls:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
