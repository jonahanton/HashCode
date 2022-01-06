from traffic_light import TrafficLight
from street import Street
from intersection import Intersection
from map import Map

from statistics import median


class ScheduleOptimizer:

    def __init__(self, map):
        self.map = map


    def manual_fit(self, schedules):
        for id, intersection in self.map.intersections.items():
            schedule = schedules[id]
            intersection.update_schedule(schedule)
        
        return self.map

    
    def naive_fit(self):

        for id, intersection in self.map.intersections.items():
            schedule = []
            for street in intersection.in_streets:
                schedule.append((street.name, 1))
            intersection.update_schedule(schedule)

        return self.map

    
    def remove_jams(self, old_map):

        for id, intersection in self.map.intersections.items():
            jam_times = []
            for street in intersection.in_streets:
                jam_time = old_map.streets[street.name].jam_time
                jam_times.append(jam_time)
            med = median(jam_times)

            for street in intersection.in_streets:
                index = [y[0] for y in intersection.schedule].index(street.name)

                jam_time = old_map.streets[street.name].jam_time
                if jam_time >= med:
                    intersection.schedule[index] = (intersection.schedule[index][0],\
                                                    intersection.schedule[index][1] + 1)
                else:
                    if intersection.schedule[index][1] > 0:
                        intersection.schedule[index] = (intersection.schedule[index][0],\
                                                    intersection.schedule[index][1] - 1)
        
        return self.map


            