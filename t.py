import threading
import time

done = False

def worker(text):
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(f"{text}, {counter}") # Print the text and counter

threading.Thread(target=worker, daemon=True, args=("Worker A",)).start() #the args parameter is a tuple of arguments to pass to the worker function. The , after "Worker A" is required to make it a tuple.
threading.Thread(target=worker, daemon=True, args=("Worker B",)).start()
threading.Thread(target=worker, daemon=True, args=("Worker C",)).start()
# worker() # worker is now running in a separate thread

input("Press enter to quit")

done = True

# print("Starting thread")    
# thread = threading.Thread(target=worker)
# thread.start()

