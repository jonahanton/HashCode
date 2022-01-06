class Street:
    
    def __init__(self, name, start, end, time):
        self.name = name
        self.start = start
        self.end = end
        self.time = time
        self.queue = []

        self.jam_time = 0
    

    def __repr__(self):
        return f"Street({self.name}, {self.start}->{self.end}, {self.time})"