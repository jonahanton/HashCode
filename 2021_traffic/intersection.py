from traffic_light import TrafficLight
from collections import deque

class Intersection:

    def __init__(self, id, in_streets=None, out_streets=None):
        self.id = id
        if in_streets is None:
            in_streets = []
        if out_streets is None:
            out_streets = []
        self.in_streets = in_streets
        self.out_streets = out_streets

        self.traffic_lights = {}
        

    def update_schedule(self, schedule):
        # Initiate traffic lights according to schedule
        self.schedule = schedule
        for street_name, duration in self.schedule:
            self.traffic_lights[street_name] = TrafficLight(0, duration)


    def __repr__(self):
        in_street_names = [street.name for street in self.in_streets]
        out_street_names = [street.name for street in self.out_streets]
        
        return f"Intersection({self.id}, in={in_street_names}, out={out_street_names}, schedule={self.schedule})"


