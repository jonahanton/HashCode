import argparse
from collections import deque

from map import Map


def run_simulation(map):

    # Initiate all schedules for every intersection to be a fixed length deque
    for id, intersection in map.intersections.items():
        period = len(intersection.in_streets)
        intersection.schedule = deque([None]*period, maxlen=period)

            
    # Keep track of cars in transit between traffic lights
    transit_cars = []
    # Keep track of cars that have reached their destination
    finished_cars = []

    T = 0
    while T <= map.D:
        print(f"Time-step {T} / {map.D}")

        # Check if any cars in transit have reached the end of the street
        # If so (and car has not finished its journey), append to end of queue
        for car, init_T in transit_cars:
            if (T - init_T) >= map.streets[car.loc].time:
                transit_cars.remove((car, init_T))
                if not car.is_at_end():
                    map.streets[car.loc].queue.append(car)
                else:
                    finished_cars.append((car, T))


        # Loop over all cars
        for car in map.cars:
            if (car not in transit_cars) and (car not in finished_cars):

                # Check if car is at front of the queue
                if len(map.streets[car.loc].queue) > 0:
                    if car.id == map.streets[car.loc].queue[0].id:

                        # Find which intersection car is waiting at
                        rel_intersection = map.intersections[map.streets[car.loc].end]

                        period = len(rel_intersection.schedule)
                        curr_green_index = T % period

                        # Check if street car is on has been assigned in the schedule
                        if rel_intersection.schedule.count(car.loc) > 0:
                            pass
                        
                        # If street yet to be assigned
                        else:
                            # Assign street to the nearest empty slot in schedule
                            i = 0
                            while True:
                                if rel_intersection.schedule[(curr_green_index+i) % period] is None:
                                    rel_intersection.schedule[(curr_green_index+i) % period] = car.loc
                                    break
                                i += 1
                            
                        # Now move car if green light
                        if rel_intersection.schedule.index(car.loc) == curr_green_index:
                            
                            # Remove car from queue
                            map.streets[car.loc].queue.pop(0)
                            # Update car location
                            car.update_loc()
                            # Add car to list of cars in transit between traffic lights
                            transit_cars.append((car, T))


        # Increment time 
        T += 1


    score = 0
    for car, T in finished_cars:
        score += (map.F + (map.D - T))

    return score





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str,
                         help="Input filepath containing .txt file containing data\
                               for simulation")
    args = parser.parse_args()
    filepath = args.filepath


    map = Map(filepath)
    score = run_simulation(map)
    print(f"Total score: {score}")

    
    

