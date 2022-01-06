from street import Street
from intersection import Intersection
from car import Car

from copy import deepcopy

class Map:

    def __init__(self, filepath):
        """
            - intersections: a dictionary that indexes Intersections instances by their id (key=id, value=Intersection)
            - streets: a dictionary of that indexes Street instances by their name (key=name, value=Street)
            - cars: a list of car instances (list of Cars)

        """
        self.intersections = {}
        self.streets = {}
        self.cars = []

        self._import_from_file(filepath)


    def _import_from_file(self, filepath):

        with open(filepath, "r") as file:

            line = file.readline().strip().split()
            line = [int(i) for i in line]
            D, I, S, V, F = line
            self.D = D
            self.I = I
            self.S = S
            self.V = V
            self.F = F

            # Initiate all Intersection instances 
            for i in range(I):
                self.intersections.setdefault(i, Intersection(id=i))
            
            # Import and initiate all Street instances
            for i in range(S):
                line = file.readline().strip().split()
                start, end, name, time = line
                start = int(start)
                end = int(end)
                time = int(time)
                self.streets[name] = Street(name, start, end, time)

            # Import and initiate all Car instances
            relevant_streets = set()
            for i in range(V):
                line = file.readline().strip().split()
                path = line[1:]
                self.cars.append(Car(i, path))
                for street_name in path:
                    relevant_streets.add(street_name)


        for street in self.streets.values():
            
            # Only consider streets that are traversed by cars
            if street.name in relevant_streets:

                # Update Street instances with queues from starting locations of Cars
                street.queue = [car for car in self.cars if car.loc == street.name]

                # Update Intersection instances with in_streets and out_streets
                start_id = street.start
                start_intersection = deepcopy(self.intersections[start_id])
                start_intersection.out_streets.append(street)
                self.intersections[start_id] = Intersection(start_id, start_intersection.in_streets, start_intersection.out_streets)
                
                end_id = street.end
                end_intersection = deepcopy(self.intersections[end_id])
                end_intersection.in_streets.append(street)
                self.intersections[end_id] = Intersection(end_id, end_intersection.in_streets, end_intersection.out_streets)
        

        # Only keep relevant intersections
        for id, intersection in list(self.intersections.items()):
            if len(intersection.in_streets) == 0 :
                del self.intersections[id]
    

    def __repr__(self):
        return f"Map({len(self.streets)} streets, {len(self.cars)} cars, {len(self.intersections)} (rel) intersections)"