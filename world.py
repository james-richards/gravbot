# World is an ordered list of chunks.
# current chunk is where the current player is
# simulate the current, previous and next chunks

from entity import Entity
from panda3d.core import Point2, Point3

chunklength = 200

class World():
  def __init__(self, app):
    self.chunks = list()

    self.worldSize = 6
     
    self.chunks.append(Chunk(app, 0, start = True)) 

    for i in range (0, self.worldSize-1):
      self.chunks.append(Chunk(app, i))

    self.chunks.append(Chunk(app, self.worldSize-1, end = True))
    
    self.currentChunk = 0

    # upper and lower rails

  def update(self, timer):
    self.chunks[self.currentChunk].update()

    if self.currentChunk > 0:
      self.chunks[self.currentChunk-1].update()
    if self.currentChunk < self.worldSize:
      self.chunks[self.currentChunk+1].update()

class Chunk():
  chunklength = 200
  def __init__(self, app, rank, start=False, end=False):
    # store enemies, bits of terrain and bullets
    self.rank = rank
    self.app = app
    self.entities = list()

    self.bg = self.app.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(rank*200.0,0))
    # indestructible rails top and bottom
    for i in range(-10, 10):
      self.entities.append(Rail(app, rank * chunklength + i * 10, top=1))
      self.entities.append(Rail(app, rank * chunklength + i * 10, top=-1))

    if(start):
      #put a wall at the start
      startwall1 = Rail(app, -100, top=0.6)
      startwall1.obj.setHpr(Point3(0,0,90))
      startwall2 = Rail(app, -100, top=0)
      startwall2.obj.setHpr(Point3(0,0,90))
      startwall3 = Rail(app, -100, top=-0.6)
      startwall3.obj.setHpr(Point3(0,0,90))

      # load a background for unplayable area
      prebg = self.app.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(-200,0))


      return
    if(end):
      #put a door at the end
      return
    return
  
  def update(self, timer):
    # this has all the bits of wall
    # maybe the enemies too
    # possibly projectiles.
    for entity in self.entities:
      entity.update()


class Rail(Entity):
  def __init__(self, app, posX, top=1):
    super(Rail, self).__init__()
    self.obj = app.loadObject("rail", depth=55, scaleX=10.0, scaleY=1.0, pos=Point2(0+posX,top*14.5))

  # Rails don't do much 
  def update(self, timer):
    return






