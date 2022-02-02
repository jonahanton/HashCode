from utils.ride import Ride
from utils.car import Car


def import_data(filename):
    with open(filename, 'r') as f:
        meta = f.readline().rstrip()
        [R, C, F, N, B, T] = [int(i) for i in meta.split(' ')]
        rides = []
        for i in range(N):
            tmp = f.readline().rstrip()
            [start1, start2, end1, end2, earliest_start, latest_finish] = [int(i) for i in tmp.split(' ')]
            rides.append(Ride((start1, start2), (end1, end2), earliest_start, latest_finish, i))
        cars = []
        for i in range(F):
            cars.append(Car(i))
    return [R, C, F, N, B, T, rides, cars]
