# All world objects
# just an interface for update and a location


class Entity(object):
    def __init__(self):
        self.location = None 
 
    def update(self, timer):
        return True


