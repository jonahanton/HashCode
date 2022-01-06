class TrafficLight:
    
    def __init__(self, state, duration):
        self.state = state
        self.duration = duration
        self.counter = 0

    
    def __repr__(self):
        return f"TrafficLight({self.state}, {self.duration})"


    def flip(self):
        self.state = (self.state + 1) % 2

    
    def increment_counter(self):
        self.counter += 1

    
    def reset_counter(self):
        self.counter = 0


