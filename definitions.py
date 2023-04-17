import time
import random
import threading
import queue
from clases import Car, FuelPump, PaymentQueue

# Función que simula el proceso de llenado del tanque
def fueling():
    car = Car(1)
    fuel_pump = FuelPump(1)
    fuel_pump.semaphore.acquire()
    car.fueling_start_time = time.time()
    print(f"Car {car.id} starts fueling at {car.fueling_start_time:.2f}")
    time.sleep(random.uniform(5, 10))
    car.fueling_end_time = time.time()
    print(f"Car {car.id} ends fueling at {car.fueling_end_time:.2f}")
    fuel_pump.semaphore.release()


# Función que simula el proceso de pago
def payment(car):
    car = Car()
    PaymentQueue.add_to_queue(car)
    while car.payment_start_time == 0:
        if PaymentQueue.queue[0] == car:
            car.payment_start_time = time.time()
            print(f"Car {Car.id} starts payment at {Car.payment_start_time:.2f}")
            time.sleep(3)
            car.payment_end_time = time.time()
            print(f"Car {Car.id} ends payment at {Car.payment_end_time:.2f}")
            PaymentQueue.remove_from_queue()

# Función que simula la llegada de los coches
def car_arrival(cars, fuel_pump, payment_queue):
    car_id = 1
    while True:
        car = Car(car_id)
        car_id += 1
        cars = []
        cars += car
        time.sleep(random.uniform(0, 15))

        # Entra en la gasolinera y comienza a repostar
        car.fueling_start_time = time.time()
        print(f"Car {car.id} arrives at the gas station at {car.arrival_time:.2f}")
        threading.Thread(target=fueling, args=(car, fuel_pump)).start()

        # Se pone en la cola de pago
        threading.Thread(target=payment, args=(car, payment_queue)).start()

# Función que calcula el tiempo medio de un coche en la gasolinera
def calculate_average_time(cars):
    total_time = 0
    for car in cars:
        total_time += Car.payment_end_time - Car.arrival_time
    return total_time / len(cars)

# Simulación con un único surtidor
def simulation_one_pump():
    fuel_pump = FuelPump(1)
    payment_queue = PaymentQueue()
    cars = queue.Queue()

    threading.Thread(target=car_arrival, args=(cars, fuel_pump, payment_queue))

fueling()
