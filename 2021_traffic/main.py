import argparse

from map import Map
from schedule import ScheduleOptimizer


def run_simulation(map):

    # Initialise one traffic light per intersection to be green
    for id, intersection in map.intersections.items():
        to_flip = intersection.schedule[0][0]
        intersection.traffic_lights[to_flip].flip()
            
    # Keep track of cars in transit between traffic lights
    transit_cars = []
    # Keep track of cars that have reached their destination
    finished_cars = []

    T = 0
    while T <= map.D:
        # print(f"Time-step {T} / {map.D}")

        # Check if any cars in transit have reached the end of the street
        # If so (and car has not finished its journey), append to end of queue
        for car, init_T in transit_cars:
            if (T - init_T) >= map.streets[car.loc].time:
                transit_cars.remove((car, init_T))
                if not car.is_at_end():
                    map.streets[car.loc].queue.append(car)
                else:
                    finished_cars.append((car, T))


        # Loop over all intersections
        curr_green_streets = []
        for id, intersection in map.intersections.items():

            # Get traffic light obj and name of street which currently has a green light at intersection
            green_street = None
            green_light = None
            for street, traffic_light in intersection.traffic_lights.items():
                if traffic_light.state == 1:
                    green_street = street
                    green_light = traffic_light
                else:
                    # Keep track of jammed cars waiting
                    if len(map.streets[street].queue) > 0:
                        map.streets[street].jam_time += 1

            if green_street is not None:

                # Store street name which currently has a green light
                curr_green_streets.append(green_street)

                # Now update traffic lights for next time-step
                # Increment counter for the green light
                green_light.increment_counter()

                index_in_schedule = [y[0] for y in intersection.schedule].index(green_street)
                # If duration of schedule for this traffic light has elapsed, 
                # change traffic light to red and make next traffic light in schedule green
                if green_light.counter >= green_light.duration:
                    green_light.reset_counter()
                    green_light.flip()
                    # Find next traffic light with duration > 0 
                    while True:
                        index_in_schedule = (index_in_schedule+1) % len(intersection.schedule)
                        if intersection.schedule[index_in_schedule][1] > 0:
                            break
                    # Make this traffic light green
                    new_green_street = intersection.schedule[index_in_schedule][0]
                    intersection.traffic_lights[new_green_street].flip()


        # Move cars
        for street_name in curr_green_streets:
            street = map.streets[street_name]
            # If there are cars waiting
            if len(street.queue) > 0:
                # Remove car at front of queue from queue
                car = street.queue.pop(0)
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
    map = ScheduleOptimizer(map).naive_fit()
    score = run_simulation(map)

    
    

