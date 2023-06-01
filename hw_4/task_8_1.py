import requests
import threading
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
        filename = 't_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
        with open(filename, "w", encoding='utf-8') as f:
            f.write(response.text)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")
    except Exception:
        print('Check URL')


threads = []
start_time = time.time()
for url in urls:
    thread = threading.Thread(target=download, args=[url])
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
