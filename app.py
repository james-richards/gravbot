from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Point2, Texture, NodePath, CollisionRay, Vec3

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode

from entity import Entity
from player import Player
from world import World

import sys

SPRITE_POS = 20 

class App(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    self.entities = dict()
    self.entities["player"] = Player(self)
    self.entities["player"].initialise()

    self.taskMgr.add(self.update, "update")
    #self.taskMgr.add(self.mouseCap, "mouseCap")
    self.bg = self.loadObject(tex = "stars", scaleX = 200, scaleY = 200, depth = 100, transparency = False)

    self.accept("a", self.entities["player"].moveLeft, [True])
    self.accept("a-up", self.entities["player"].moveLeft, [False])

    self.accept("d", self.entities["player"].moveRight, [True])
    self.accept("d-up", self.entities["player"].moveRight, [False])

    self.accept("space", self.entities["player"].jump, [])

    self.accept("mouse1", self.entities["player"].activate, [])

    self.accept("escape", sys.exit, [])

    self.prevTime = 0

    self.mousePos = Point2()

    self.rl = base.camLens.makeCopy()

    self.world = World(self)


  def update(self, task):
    delta = task.time - self.prevTime
    self.prevTime = task.time

    if(base.mouseWatcherNode.hasMouse()):
      self.mousePos.x = self.mouseWatcherNode.getMouseX()
      self.mousePos.y = self.mouseWatcherNode.getMouseY()

    for entity in self.entities:
      self.entities[entity].update(delta)
    return Task.cont

  def mouseCap(self, task):
    if(base.mouseWatcherNode.hasMouse()):
      self.mousePos.x = self.mouseWatcherNode.getMouseX()
      self.mousePos.y = self.mouseWatcherNode.getMouseY()
    return Task.cont  

  def loadObject(self, tex = None, pos = Point2(0,0), depth = SPRITE_POS, transparency = True, scaleX = 1, scaleY = 1, scale = None):
    obj = self.loader.loadModel("models/plane") 
    obj.reparentTo(self.render)
                                     
    obj.setPos(Point3(pos.getX(), depth, pos.getY())) 

    if (scale == None):
      obj.setScale(scaleX, 1, scaleY)
    else:
      obj.setScale(scale)

    obj.setBin("unsorted", 0) # ignore draw order (z-fighting fix)       
    obj.setDepthTest(True)   # Don't disable depth write like the tut says
                            
    if transparency: obj.setTransparency(1) #All of our objects are trasnparent
    if tex:
      tex = loader.loadTexture("textures/"+tex+".png") #Load the texture
      tex.setWrapU(Texture.WMClamp)                    # default is repeat, which will give
      tex.setWrapV(Texture.WMClamp)                    # artifacts at the edges
      obj.setTexture(tex, 1)                           #Set the texture

    return obj

  def quit(self):
    sys.exit()

app = App()
app.run()

