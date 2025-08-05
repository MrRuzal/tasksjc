'''
Параллельная обработка числовых данных
азработайте программу, которая выполняет следующие шаги:

Сбор данных:

Создайте функцию generate_data(n), которая генерирует список из n случайных целых
чисел в диапазоне от 1 до 1000. Например, generate_data(1000000) должна вернуть
список из 1 миллиона случайных чисел.

Обработка данных:

Напишите функцию process_number(number), которая выполняет вычисления над числом.
Например, вычисляет факториал числа или проверяет, является ли число простым.
Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы продемонстрировать
преимущества мультипроцессинга.

Параллельная обработка:

Используйте модули multiprocessing и concurrent.futures для параллельной обработки списка чисел.

Реализуйте три варианта:

Вариант А: Ипользование пула потоков с concurrent.futures.

Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.

Вариант В: Создание отдельных процессов с использованием multiprocessing.Process
и очередей (multiprocessing.Queue) для передачи данных.

Сравнение производительности:

Измерьте время выполнения для всех вариантов и сравните их с однопоточным
(однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.

Сохранение результатов:

Сохраните обработанные данные в файл (например, в формате JSON или CSV).
'''

import random
import time
import math
import csv
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Process, Queue, cpu_count


def generate_data(n: int) -> list[int]:
    """Генерация n случайных чисел от 1 до 1000."""
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(n: int) -> bool:
    """Проверка, является ли число простым."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def run_single_thread(data: list[int]) -> list[bool]:
    return [process_number(x) for x in data]


def run_thread_pool(data: list[int]) -> list[bool]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))


def run_process_pool(data: list[int]) -> list[bool]:
    with multiprocessing.Pool(processes=cpu_count()) as pool:
        return pool.map(process_number, data)


def worker(input_q: Queue, output_q: Queue) -> None:
    while True:
        item = input_q.get()
        if item is None:
            break
        output_q.put(process_number(item))


def run_manual_processes(data: list[int]) -> list[bool]:
    input_q = Queue()
    output_q = Queue()
    workers = [
        Process(target=worker, args=(input_q, output_q))
        for _ in range(cpu_count())
    ]

    for p in workers:
        p.start()

    for item in data:
        input_q.put(item)

    for _ in workers:
        input_q.put(None)

    results = [output_q.get() for _ in data]

    for p in workers:
        p.join()

    return results


def save_to_csv(data: list[int], results: list[bool], filename: str) -> None:
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['number', 'is_prime'])
        writer.writerows(zip(data, results))


def print_timings_table(timings: dict[str, float]) -> None:
    print("Метод,Время выполнения (секунды)")
    for method, duration in timings.items():
        print(f"{method},{duration:.2f}")


def main():
    size = 100_000
    data = generate_data(size)
    timings = {}

    start = time.time()
    result = run_single_thread(data)
    timings['Single-thread'] = time.time() - start
    save_to_csv(data, result, 'results_single.csv')

    start = time.time()
    result = run_thread_pool(data)
    timings['ThreadPoolExecutor'] = time.time() - start
    save_to_csv(data, result, 'results_threadpool.csv')

    start = time.time()
    result = run_process_pool(data)
    timings['ProcessPoolExecutor'] = time.time() - start
    save_to_csv(data, result, 'results_processpool.csv')

    start = time.time()
    result = run_manual_processes(data)
    timings['ManualProcess+Queue'] = time.time() - start
    save_to_csv(data, result, 'results_manual.csv')

    print_timings_table(timings)


if __name__ == '__main__':
    main()
