import threading
import time
import random
import queue

# Definimos los estados de un coche
class Car:
    def __init__(self, id):
        self.id = id
        self.arrival_time = time.time()
        self.fueling_start_time = 0
        self.fueling_end_time = 0
        self.payment_start_time = 0
        self.payment_end_time = 0

# Definimos el surtidor como un semáforo con N permisos
class FuelPump:
    def __init__(self, n):
        self.semaphore = threading.Semaphore(n)

# Definimos la cola de pago como una cola FIFO
class PaymentQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def add_to_queue(self, car):
        self.queue.put(car)

    def remove_from_queue(self):
        return self.queue.get()

