# encoding: utf-8
from fabric.api import task
import multiprocessing
import time

def is_cpu_max(i):
    return i >= multiprocessing.cpu_count()

def print_name(name, lock, num):
    if is_cpu_max(num) is True:
        lock.acquire()
        # 何らかの時間のかかる処理を想定してsleep
        print(name)
        time.sleep(1)
        lock.release()
    else:
        print(name)

    num -= 1

def worker(names):
    jobs = []
    lock = multiprocessing.Lock()
    worker_num = 1

    for module in names:
        worker_num += 1
        job = multiprocessing.Process(target=print_name, args=(str(module), lock, worker_num), )
        jobs.append(job)
        job.start()

    [job.join() for job in jobs]

@task
def main():
    """CPUコア数までプロセスを生成して処理する"""
    """最大数まで生成したらロックして他処理の終了を待つ"""
    start = time.time();

    worker(xrange(20))

    elapsed_time = time.time() - start

    print("elapsed_time:{0}".format(elapsed_time)) + "[sec]"

