from math import degrees, sin, cos
from panda3d.core import Point2, BoundingSphere
from entity import Entity


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
    self.app.world.addEntity(Flame(self.app, self.obj.getPos(self.app.render), self.obj.getHpr()))
    return True

  def update(self, timer):
    self.obj.setHpr(self.player.obj, 0, 0, -1 * degrees(self.player.angle))

# The thing that comes out the end
class Flame(Entity):
  animspeed = 0.1 
  depth = 55
  playerWidth = 3
  speed = 40
  def __init__(self, app, pos, hpr):
    super(Flame, self).__init__()

    self.anim = list()
    self.anim.append(app.loadObject("flame1", depth=Flame.depth))
    self.anim.append(app.loadObject("flame2", depth=Flame.depth))
    self.anim.append(app.loadObject("flame3", depth=Flame.depth))

    for a in self.anim:
      a.hide()

    self.app = app
    self.curspr = 0
    self.obj = self.anim[self.curspr]
    self.obj.show() 
    self.delta = 0

    self.pos = pos
    self.pos.y = Flame.depth
    self.hpr = hpr
    self.vel = Point2()
    self.vel.x = cos(app.world.player.angle)*Flame.speed
    self.vel.y = sin(app.world.player.angle)*Flame.speed

    self.vel.x += app.world.player.velocity.x
    
    #self.pos.x += 4  
    #self.pos.z += 2
    self.pos.x = self.vel.x / Flame.speed * 2+ self.pos.x
    self.pos.z = self.vel.y / Flame.speed * 2+ self.pos.z

    self.bounds.append(BoundingSphere(self.pos, 0.5))
    # print self.pos
    #print hpr
    #print self.vel

  def update(self, timer):
    #animation
    self.delta += timer

    if self.delta > Flame.animspeed:
      self.delta = 0
      self.obj.hide()
      self.curspr += 1
      if self.curspr > len(self.anim)-1:
        self.curspr = 0
    self.obj = self.anim[self.curspr]
    self.obj.show()

    self.pos.x = self.vel.x * timer + self.pos.x
    self.pos.z = self.vel.y * timer + self.pos.z

    self.obj.setPos(self.pos.x, self.pos.y, self.pos.z)
    self.obj.setHpr(self.hpr)

    s = self.obj.getBounds()
    self.bounds[0] = BoundingSphere(s.getCenter(), s.getRadius())


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
    
