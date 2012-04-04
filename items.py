from math import degrees
from panda3d.core import Point2


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

class Blowtorch(Item):
  def __init__(self, app, player):
    super(Blowtorch, self).__init__(app, player)
    self.obj = app.loadObject("blowtorch", scaleX = 1, scaleY = 1, depth = -0.2)
    self.obj.hide()

    self.flame1 = app.loadObject("torchflame1", pos=Point2(1,0.01),scaleX = 1, scaleY = 0.125, depth = -0.1)
    self.flame2 = app.loadObject("torchflame2", pos=Point2(1,0.01),scaleX = 1, scaleY = 0.125, depth = -0.1)
    self.flame3 = app.loadObject("torchflame3", pos=Point2(1,0.01),scaleX = 1, scaleY = 0.125, depth = -0.1)
    self.curFlame = 1
    self.flameHidden = True
    self.flame1.reparentTo(self.obj)
    self.flame2.reparentTo(self.obj)
    self.flame3.reparentTo(self.obj)
    self.flame1.hide()
    self.flame2.hide()
    self.flame3.hide()
    self.delta = 0
    self.changeAfter = 0.3 

  def activate(self):
    if (self.flameHidden):
      self.flame1.show()
      self.flameHidden = False
    else: 
      self.flame1.hide()  
      self.flame2.hide()  
      self.flame3.hide()  
      self.flameHidden = True
    return True

  def update(self, timer):
    self.obj.setHpr(self.player.obj, 0, 0, -1 * degrees(self.player.angle))
    self.delta += timer
    if self.delta > self.changeAfter:
      self.curFlame += 1
      if (self.curFlame == 4):
        self.curFlame = 1

      self.flame1.hide()
      self.flame2.hide()
      self.flame3.hide()

      if not self.flameHidden: getattr(self, "flame" + str(self.curFlame)).show()
      self.delta = 0
    


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
    
