import threading
import multiprocessing
import time
import numpy as np
import pickle


DATA = np.random.randn(10000, 10000)


def dummy_task(name):
    print(f"{name} started")
    time.sleep(20)
    print(f"{name} finished")


def input_output_intensive_task(name):
    print(f"{name} started")
    with open("data", "wb") as f:
        pickle.dump(DATA, f)
    print(f"{name} finished")


def cpu_intensive_task(name):
    print(f"{name} started")
    result = np.sum(DATA)
    print(f"{name} finished")


def baseline_example():
    print("Starting single process/thread...")
    for i in range(4):
        dummy_task(f"Baseline-{i+1}")
    print("Single process/thread completed.")


# Using threading
def threading_example():
    print("Starting threads...")
    threads = []
    for i in range(4):
        thread = threading.Thread(target=dummy_task, args=(f"Thread-{i+1}",))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Threads completed.")


# Using multiprocessing
def multiprocessing_example():
    print("Starting processes...")
    processes = []
    for i in range(4):
        process = multiprocessing.Process(target=dummy_task, args=(f"Process-{i+1}",))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print("Processes completed.")


if __name__ == "__main__":


    print("Comparing threading and multiprocessing:")

    for task_type in ['input_output', 'cpu_intensive']:
        for optimization_method in ['baseline', 'threading', 'multiprocessing']:



    print("\n--- Baseline Example (no threading, no multiprocessing)---")
    start = time.time()
    baseline_example()
    end = time.time()
    print(f"Threading execution time: {end - start:.2f} seconds")

    print("\n--- Threading Example ---")
    start = time.time()
    threading_example()
    end = time.time()
    print(f"Threading execution time: {end - start:.2f} seconds")

    print("\n--- Multiprocessing Example ---")
    start = time.time()
    multiprocessing_example()
    end = time.time()
    print(f"Multiprocessing execution time: {end - start:.2f} seconds")
