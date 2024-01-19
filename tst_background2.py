import threading
import time
from multiprocessing import Process, Queue

tasks = []
results = []


def background_operation(url, url_filter, result_queue):
    # Perform some time-consuming operation
    print("gui   : background_operation for \"" + url + "\"")
    # data = coordinator.Coordinator().query(url, url_filter)
    data = ""
    print("gui   : background_operation ...")
    time.sleep(2)
    print("gui   : background_operation ...")
    time.sleep(2)
    print("gui   : background_operation ...")
    time.sleep(2)
    print("gui   : background_operation DONE")
    # Add result to the queue
    result_queue.put(data)


def create_task(url, url_filter):
    print("gui   : create_task for \"" + url + "\"")
    # Create a queue to store the result
    result_queue = Queue()
    # Start the background operation in a separate process
    process = threading.Thread(target=background_operation, args=(url, url_filter, result_queue))
    process.start()
    # Add the process and result queue to the tasks list
    tasks.append((process, result_queue))


def task_result():
    # Check each task in the tasks list
    for task in tasks:
        process, result_queue = task
        # Check if the background operation has finished
        if not process.is_alive():
            result = result_queue.get()  # Get the result from the queue
            results.append(result)  # Add the result to the results list
            tasks.remove(task)  # Remove the task from the tasks list
            process.terminate()  # Terminate the process
