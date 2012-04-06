# All world objects
# just an interface for update and a location

class Entity(object):
    def __init__(self):
        self.location = None 
	self.obj = None
	self.bounds = list()
 
    def update(self, timer):
        return True

    def collideWith(self, entity):

        r =  self.obj.getBounds().contains(entity.obj.getBounds())
	if r != 0:
	  print r
        for bound1 in self.bounds:
	  for bound2 in entity.bounds:
	     print bound1.contains(bound2)


