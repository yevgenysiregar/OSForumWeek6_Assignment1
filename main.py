import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_finished = False
even_numbers = []
odd_numbers = []

class Producer(threading.Thread):
    def run(self):
        global buffer, producer_finished
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            with lock:
                buffer.append(num)
                with open("all.txt", "a") as f:
                    f.write(str(num) + "\n")
        producer_finished = True

class Customer(threading.Thread):
    def __init__(self, is_even):
        super().__init__()
        self.is_even = is_even

    def run(self):
        global buffer, producer_finished, even_numbers, odd_numbers
        while not producer_finished or buffer:
            with lock:
                if buffer:
                    num = buffer.pop()
                    if num % 2 == 0:
                        even_numbers.append(num)
                    else:
                        odd_numbers.append(num)
                    filename = "even.txt" if self.is_even else "odd.txt"
                    with open(filename, "a") as f:
                        f.write(str(num) + "\n")

if __name__ == "__main__":
    producer = Producer()
    customer1 = Customer(is_even=True)
    customer2 = Customer(is_even=False)

    producer.start()
    customer1.start()
    customer2.start()

    producer.join()
    customer1.join()
    customer2.join()

    print("Terminating program, successfully completed.")
