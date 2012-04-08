# World is an ordered list of chunks.
# current chunk is where the current player is
# simulate the current, previous and next chunks

from entity import Entity
from panda3d.core import Point2, Point3, BoundingBox, BoundingSphere, Vec3
from panda3d.core import PerlinNoise2
from player import Player
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode

import utilities

worldsize = Point2(30,30)

class World():
  def __init__(self, size):

    self.bw = BulletWorld()
    self.bw.setGravity(0,0,-9.8)
    self.size = size
    self.perlin = PerlinNoise2()

    self.player = Player(self)
    self.player.initialise()

    self.entities = list()
    self.bgs = list()
    self.makeChunk(Point2(0,0)) 

    # the lower rail
    shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
    self.groundNode = BulletRigidBodyNode('Ground')
    self.groundNode.addShape(shape)
    self.groundnp = render.attachNewNode(self.groundNode)
    self.groundnp.setPos(0, 0, 0)
    self.bw.attachRigidBody(self.groundNode)

  def update(self, timer):
    dt = globalClock.getDt()
    self.bw.doPhysics(dt)

    self.player.update(timer)

    for entity in self.entities:
      entity.update(timer)

  # Generate a $worldsize chunk of data with bottom left corner at $pos
  def makeChunk(self, pos):
    # store enemies, bits of terrain and projectiles in entities
    # so we can do some collision detection
    self.bgs.append(utilities.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(pos.x*worldsize.x,pos.y*worldsize.y)))
    # also need to put these around any other "edge" nodes
    #self.bgs.append(utilities.loadObject("stars", depth=100, scaleX=200, scaleY=200.0, pos=Point2(pos.x*-200,0)))

    for i in range(-10, 10):
      self.entities.append(Rail(self, i * 10, 0))
    
    pt = list()

    for i in range(0, int(worldsize.x)):
      pt.append(list())
      for j in range(0, int(worldsize.y)):
        if self.perlin.noise(i,j) > 0:
	  pt[i].append(1)
	else: pt[i].append(0)  

    pt[0][0] = 0	
    pt[1][0] = 0	
    pt[0][1] = 0	
    pt[1][1] = 0	
    pt[2][2] = 1
    pt[2][1] = 1	
    pt[1][2] = 1	
    pt[2][2] = 1

    
  def addEntity(self, entity):
    self.entities.append(entity)

class Rail(Entity):
  def __init__(self, world, posX, posY):
    super(Rail, self).__init__()
    self.obj = utilities.loadObject("rail", depth=55, scaleX=10.0, scaleY=1.0, pos=Point2(posX,posY))

  # Rails don't do much 
  def update(self, timer):
    return

class Wall(Entity):
  def __init__(self, world, pos):
    super(Wall, self).__init__()
    self.health = 100

    shape = BulletBoxShape(Vec3(0.5,2.0,0.5))
    self.bnode = BulletRigidBodyNode()
    self.bnode.addShape(shape)
    self.np = utilities.app.render.attachNewNode(self.bnode)
    self.np.setPos(pos.x,20,pos.y)
    world.bw.attachRigidBody(self.bnode)

    self.obj = utilities.loadObject("wall", depth = 0)
    self.obj.reparentTo(self.np)
    self.obj.setScale(1)

  def update(self, timer):
    if self.health < 0:
      self.obj.remove()

  def addToNode(self, pos):
    return


  def expandNode(pt):
    for i in range(1, int(worldsize.x)-1):
      for j in range(1, int(worldsize.y)-1):
       if pt[i][j] == 1:
         self.entities.append(Wall(self, Point2(i,j)))
         if pt[i-1][j-1] == 1 : 
	   self.entities[-1].addToNode(Point2(i,j))
	   pt[i][j] = -1
         if pt[i-1][j] == 1 : 
	   self.entities[-1].addToNode(Point2(i,j))
	   pt[i][j] = -1
         if pt[i-1][j+1] == 1 : 
	   self.entities[-1].addToNode(Point2(i,j))
	   pt[i][j] = -1
         if pt[i][j-1] == 1 : 
	   self.entities[-1].addToNode(Point2(i,j))
	   pt[i][j] = -1
         if pt[i][j+1] == 1 : 
	   self.entities[-1].addToNode(Point2(i,j))
	   pt[i][j] = -1
