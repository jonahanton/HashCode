from .ride import Ride
from .car import Car 

def import_data(filename):
    with open(f"data/{filename}", 'r') as f:
        lines = f.readlines()

    meta = lines[0]
    ride_strings = lines[1:]

    [R, C, F, N, B, T] = list(map(int, meta.split(' ')))
    rides = []
    
    for i, ride in enumerate(ride_strings):
        [x0, y0, x1, y1, es, lf] = list(map(int, ride.strip().split(' ')))
        rides.append(Ride((x0, y0), (x1, y1), es, lf, i))
    
    cars = []
    for i in range(F):
        cars.append(Car(i))

    return [R, C, F, N, B, T, rides, cars]


def export_data(filename, cars):
    pass