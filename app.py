from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Point2, Texture, NodePath, CollisionRay, Vec3

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode


from entity import Entity
from player import Player
from world import World
import utilities 

import sys

from pandac.PandaModules import loadPrcFileData 


SPRITE_POS = 20 

class App(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    utilities.setApp(self)

    loadPrcFileData('', 'bullet-enable-contact-events true')

    self.world = World(10)

    self.taskMgr.add(self.update, "update")

    self.accept("a", self.world.player.moveLeft, [True])
    self.accept("a-up", self.world.player.moveLeft, [False])

    self.accept("d", self.world.player.moveRight, [True])
    self.accept("d-up", self.world.player.moveRight, [False])

    self.accept("space", self.world.player.jump, [True])
    self.accept("space-up", self.world.player.jump, [False])

    self.accept("c", self.world.player.crouch, [True])
    self.accept("c-up", self.world.player.crouch, [False])

    self.accept("mouse1", self.world.player.activate, [])

    self.accept("escape", sys.exit, [])

    self.accept('bullet-contact-added', self.onContactAdded) 
    self.accept('bullet-contact-destroyed', self.onContactDestroyed) 

    self.accept("h", self.showDBG, [True])
    self.accept("h-up", self.showDBG, [False])

    self.prevTime = 0

    self.mousePos = Point2()
    base.disableMouse()

    self.rl = base.camLens.makeCopy()

    # bullet testing
    debugNode = BulletDebugNode('Debug')
    debugNode.showWireframe(True)
    debugNode.showConstraints(True)
    debugNode.showBoundingBoxes(False)
    debugNode.showNormals(False)
    self.debugNP = render.attachNewNode(debugNode)
    self.debugNP.show()

    self.world.bw.setDebugNode(self.debugNP.node())



  def update(self, task):
    delta = task.time - self.prevTime
    self.prevTime = task.time

    if(base.mouseWatcherNode.hasMouse()):
      self.mousePos.x = self.mouseWatcherNode.getMouseX()
      self.mousePos.y = self.mouseWatcherNode.getMouseY()
    self.world.update(delta)  

    return Task.cont

  def onContactAdded(self, node1, node2):
    return
    
  def onContactDestroyed(self, node1, node2):
    return

  def mouseCap(self, task):
    if(base.mouseWatcherNode.hasMouse()):
      self.mousePos.x = self.mouseWatcherNode.getMouseX()
      self.mousePos.y = self.mouseWatcherNode.getMouseY()
    return Task.cont  

  def showDBG(self, b):
    if b:
      self.debugNP.show()
    else:  
      self.debugNP.hide()

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

