
class Car:
    def __init__(self, id):
        self.id = id
        self.location = (0, 0)

        self.ride = None
        self.is_riding = False

        self.expected_start = None
        self.expected_finish = None

        self.prev_rides = list()

    @property
    def is_free(self):
        return self.ride is None

    def add_ride(self, ride, step):
        self.ride = ride

        if step == self.ride.earliest_start:
            self.ride.on_time = True

        self.expected_start = step + self.distance_to_start(ride)
        self.expected_finish = step + self.total_ride_distance(ride)

        self.location = self.ride.start

    def start_ride(self, step):
        self.ride.mark_as_started(step)
        self.is_riding = True
        self.location = self.ride.end

    def finish_ride(self, step):
        self.ride.mark_as_done(step)
        self.prev_rides.append(self.ride.id)

        finished_ride = self.ride

        self.ride = None
        self.is_riding = False

        self.expected_start = None
        self.expected_finish = None

        return finished_ride


    def check_ride_finished(self, step):
        if not self.ride:
            return False, None

        if not self.is_riding and self.expected_start <= step:
            self.start_ride(step)
            return False, None

        elif self.is_riding and self.expected_finish <= step:
            finished_ride = self.finish_ride(step)
            return True, finished_ride
            
        return False, None

    def manhatten(self, start, end):
        (x0, y0), (x1, y1) = start, end
        return abs(x1 - x0) + abs(y1 - y0)

    def distance_to_start(self, ride):
        return self.manhatten(self.location, ride.start)

    def total_ride_distance(self, ride):
        distance_to_start = self.distance_to_start(ride)
        return distance_to_start + ride.distance

    def can_finish(self, ride, step):
        total_distance = self.total_ride_distance(ride)
        return step + total_distance <= ride.latest_finish
