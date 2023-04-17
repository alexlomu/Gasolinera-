import time
import random
import threading
import queue
from clases import Car, FuelPump, PaymentQueue


# Función que simula la llegada de los coches
def car_arrival(car_id, cars):
    car_id = 0
    cars = []
    while True:
        car_id += 1
        car = Car(car_id)
        cars += car
        time.sleep(random.uniform(0, 15))

        # Entra en la gasolinera y comienza a repostar
        car.fueling_start_time = time.time()
        print(f"Car {car.id} llega a la estación: {car.arrival_time:.2f}")


# Función que simula el proceso de llenado del tanque
def fueling():
    car = Car(car_id)
    fuel_pump = FuelPump()
    fuel_pump.semaphore.acquire()
    car.fueling_start_time = time.time()
    print(f"Car {car.id} empieza a repostar: {car.fueling_start_time:.2f}")
    time.sleep(random.uniform(5, 10))
    car.fueling_end_time = time.time()
    print(f"Car {car.id} acaba de repostar: {car.fueling_end_time:.2f}")
    fuel_pump.semaphore.release()

# Función que simula el proceso de pago
def payment():
    car = Car(random.randint(0,50))
    PaymentQueue.add_to_queue(car)
    while car.payment_start_time == 0:
        if PaymentQueue.queue[0] == car:
            car.payment_start_time = time.time()
            print(f"Car {car.id} empieza a pagar {car.payment_start_time:.2f}")
            time.sleep(3)
            car.payment_end_time = time.time()
            print(f"Car {car.id} acaba de pagar: {car.payment_end_time:.2f}")
            PaymentQueue.remove_from_queue()

# Función que calcula el tiempo medio de un coche en la gasolinera
def calculate_average_time(car, cars):
    total_time = 0
    for car in cars:
        total_time += car.payment_end_time - car.arrival_time
    return total_time / len(cars)

# Simulación con un único surtidor
def simulation_one_pump():
    fuel_pump = FuelPump(4)
    payment_queue = PaymentQueue()
    cars = queue.Queue()

    threading.Thread(target=car_arrival, args=(cars, fuel_pump, payment_queue))


