from collections import deque
from threading import Lock, Thread
from time import sleep

def download(obj):
    print('download')
    sleep(0.5)

def resize(obj):
    print('resize')
    sleep(0.1)

def upload(obj):
    print('upload')
    sleep(0.3)

class Queue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self, item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            self.items.popleft()

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0

    def run(self):
        while True:
            self.polled_count += 1

            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1


if __name__ == "__main__":

    download_queue = Queue()
    resize_queue = Queue()
    upload_queue = Queue()
    threads = [
            Worker(download, download_queue, resize_queue),
            Worker(download, resize_queue, upload_queue),
            ]

    for thread in threads:
        thread.start()

    for _ in range(10000):
        download_queue.put(object())
