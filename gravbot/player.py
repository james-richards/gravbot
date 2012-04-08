from entity import Entity
from panda3d.core import Point2, Point3, NodePath, BoundingBox, Vec3, BitMask32
from items import Blowtorch, LightLaser, Grenade
from math import atan2, degrees, sin, cos
import utilities

from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode

class Player(Entity):

    walkspeed = 50
    damping = 0.9
    topspeed = 15

    leftMove = False
    rightMove = False
    jumpToggle = False
    crouchToggle = False

    def __init__(self, world):
        super(Player, self).__init__()

        self.obj = utilities.loadObject("player", depth=20)

        self.world = world 
        self.health = 100
        self.inventory = dict()

        self.depth = self.obj.getPos().y

        self.location = Point2(0,0)
        self.velocity = Vec3(0)
        self.pt = 0.0

        self.shape = BulletBoxShape(Vec3(0.3, 1.0, 0.49))
        self.bnode = BulletRigidBodyNode('Box')
        self.bnode.setMass(1.0)
        self.bnode.setAngularVelocity(Vec3(0))
        self.bnode.setAngularFactor(Vec3(0))
        self.bnode.addShape(self.shape)
        self.bnode.setLinearDamping(0.95)
        self.bnode.setLinearSleepThreshold(0)

        world.bw.attachRigidBody(self.bnode)
        self.bnode.setPythonTag("Entity", self)
        self.bnode.setIntoCollideMask(BitMask32.bit(0))

        self.node = utilities.app.render.attachNewNode(self.bnode)
        self.node.setPos(self.obj.getPos())

        self.obj.setPos(0,0,0)
        self.obj.setScale(1)
        self.obj.reparentTo(self.node)
        self.node.setPos(self.location.x, self.depth, self.location.y)

    def initialise(self):
        self.inventory["LightLaser"] = LightLaser(self.world, self)
        self.inventory["Blowtorch"] = Blowtorch(self.world, self)
        self.inventory["Grenade"] = Grenade(self.world, self)

        for i in self.inventory:
            self.inventory[i].initialise()

        self.currentItem = self.inventory["Blowtorch"]
        self.currentItem.equip()

        self.armNode = self.obj.attachNewNode("arm")
        self.armNode.setPos(0.20,0,0.08)
        self.arm = utilities.loadObject("arm", scaleX = 0.5,scaleY = 0.5, depth = -0.2)
        self.arm.reparentTo(self.armNode)

    def activate(self):
        self.currentItem.activate()

    def update(self, timer):
        self.velocity = self.bnode.getLinearVelocity()

        if (self.leftMove):
            self.bnode.applyCentralForce(Vec3(-Player.walkspeed,0,0))
        if (self.rightMove):
            self.bnode.applyCentralForce(Vec3(Player.walkspeed,0,0))
        if (self.jumpToggle):
            self.bnode.applyCentralForce(Vec3(0,0,Player.walkspeed))
        if (self.crouchToggle):
            self.bnode.applyCentralForce(Vec3(0,0,-Player.walkspeed))
        
        if (self.velocity.x < -self.topspeed):
            self.velocity.x = -self.topspeed
        if (self.velocity.x > self.topspeed):
            self.velocity.x = self.topspeed

        mouse = utilities.app.mousePos
        # extrude test
        near = Point3()
        far = Point3()
        utilities.app.camLens.extrude(mouse, near, far)
        camp = utilities.app.camera.getPos()
        near *= 20 # player depth

        if near.x != 0:
            angle = atan2(near.z + camp.z - self.node.getPos().z, near.x + camp.x - self.node.getPos().x)
            #angle = atan2(near.z, near.x)
        else:
            angle = 90  

        self.angle = angle

        # set current item to point at cursor   
        self.currentItem.update(timer)

        # move the camera so the player is centred horizontally,
        # but keep the camera steady vertically
        utilities.app.camera.setPos(self.node.getPos().x, 0, self.node.getPos().z)

        #move arm into correct position.

        gunLength = 2.0

        self.gunVector = Point2(cos(angle)*gunLength - self.armNode.getX()*5, sin(angle)*gunLength - self.armNode.getZ()*2)
        armAngle = atan2(self.gunVector.y, self.gunVector.x)
        self.arm.setHpr(self.armNode, 0, 0, -1 * degrees(armAngle))

    def moveLeft(self, switch):
        self.leftMove = switch 
        #self.bnode.applyCentralForce(Vec3(-500,0,0))

    def moveRight(self, switch):
        self.rightMove = switch 
        #self.bnode.applyCentralForce(Vec3(500,0,0))

    def jump(self, switch):
        self.jumpToggle = switch

    def crouch(self, switch):
        self.crouchToggle = switch

