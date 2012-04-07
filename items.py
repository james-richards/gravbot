from math import degrees, sin, cos
from panda3d.core import Point2, BoundingSphere, Vec3, Point3
from entity import Entity
from panda3d.bullet import BulletBoxShape,BulletRigidBodyNode
from inspect import getmembers

class Item(object):
  def __init__(self, app, player, charges = 1):
    self.charges = charges
    self.obj = None 
    self.app = app
    self.player = player

  def initialise(self):
    self.obj.reparentTo(self.player.obj) 

  #fired when the player clicks
  def activate(self):
    return True

  def update(self):
    return true

  def equip(self):
    self.obj.show()
    return True
  
  def unequip(self):
    self.obj.hide()
    return True

# The thing you hold
class Blowtorch(Item):
  def __init__(self, app, player):
    super(Blowtorch, self).__init__(app, player)
    self.obj = app.loadObject("blowtorch", scaleX = 1, scaleY = 1, depth = -0.2)
    self.obj.hide()

  def activate(self):
    #add a flame projectile
    self.app.world.addEntity(Flame(self.app, self.player.obj.getPos(self.app.render), self.obj.getHpr()))
    return True

  def update(self, timer):
    self.obj.setHpr(self.player.obj, 0, 0, -1 * degrees(self.player.angle))

# The thing that comes out the end
class Flame(Entity):
  animspeed = 0.1 
  depth = 20 
  playerWidth = 3
  speed = 30 
  def __init__(self, app, pos, hpr):
    super(Flame, self).__init__()

    self.shape = BulletBoxShape(Vec3(0.5,0.1,0.25))
    self.bnode = BulletRigidBodyNode()
    self.bnode.setMass(1.0)
    self.bnode.addShape(self.shape)

    self.np = app.render.attachNewNode(self.bnode)

    self.app = app
    self.anim = list()
    self.anim.append(app.loadObject("flame1", depth=0))
    self.anim.append(app.loadObject("flame2", depth=0))
    self.anim.append(app.loadObject("flame3", depth=0))
    self.app.bw.attachRigidBody(self.bnode)

    self.curspr = 0
    self.obj = self.anim[self.curspr]
    self.obj.show() 
    self.livetime = 0
    self.delta = 0

    self.pos = pos
    self.pos.y = Flame.depth
    self.hpr = hpr
    self.vel = Point2()
    self.vel.x = cos(app.world.player.angle)*Flame.speed
    self.vel.y = sin(app.world.player.angle)*Flame.speed

    tv = Vec3(self.vel.x, 0, self.vel.y)
    tv += app.world.player.bnode.getLinearVelocity()

    self.bnode.setLinearVelocity(tv)
    self.bnode.setGravity(Vec3(0,0,0))

    self.np.setHpr(hpr)
    self.np.setPos(pos)

    self.bnode.setAngularFactor(Vec3(0,0,0))
    self.bnode.setLinearFactor(Vec3(1,0,1))

    for a in self.anim:
      a.hide()
      a.reparentTo(self.np)
      a.setPos(0, -0.1,-0.3)

  def update(self, timer):
    #animation
    self.delta += timer
    self.livetime += timer

    if self.delta > Flame.animspeed:
      self.delta = 0
      self.obj.hide()
      self.curspr += 1
      if self.curspr > len(self.anim)-1:
        self.curspr = 0
    self.obj = self.anim[self.curspr]
    self.obj.show()

class Grenade(Item):
  def __init__(self, app, player):
    super(Grenade, self).__init__(app, player)
    self.obj = app.loadObject("grenade", scaleX = 1, scaleY = 2)
    self.obj.hide()

  def activate(self):
    return True
    
class LightLaser(Item):
  def __init__(self, app, player):
    super(LightLaser, self).__init__(app, player)
    self.obj = app.loadObject("lightlaser", scaleX = 1, scaleY = 2)
    self.obj.hide()

  def activate(self):
    return True
    
