from utils.ride import Ride


def import_data(filename):
    filepath = "data/" + filename
    with open(filepath, 'r') as f:
        meta = f.readline().rstrip()
        [R, C, F, N, B, T] = [int(i) for i in meta.split(' ')]
        rides = []
        for i in range(N):
            tmp = f.readline().rstrip()
            [start1, start2, end1, end2, earliest_start, latest_finish] = [int for i in tmp.split(' ')]
            rides += Ride((start1, start2), (end1, end2), earliest_start, latest_finish)
    return [R, C, F, N, B, T, rides]
