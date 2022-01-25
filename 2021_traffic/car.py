class Car:

    def __init__(self, id, path=None):
        self.id = id
        if path is None:
            path = []
        self.path = path
        if len(self.path) > 0:
            self.loc = path[0]
    

    def __repr__(self):
        return f"Car({self.id}, {self.loc})"

    
    def update_loc(self):
        self.loc = self.path[self.path.index(self.loc) + 1]

    
    def is_at_end(self):
        return self.loc == self.path[-1]

