from panda3d.core import Point2, Point3, Texture


SPRITE_POS = 55
app = None

def setApp(a):
    global app 
    app = a


def loadObject(tex = None, pos = Point2(0,0), depth = SPRITE_POS, transparency = True, scaleX = 1, scaleY = 1, scale = None):
    global app
    obj = app.loader.loadModel("models/plane")
    obj.reparentTo(app.render)

    obj.setPos(Point3(pos.getX(), depth, pos.getY()))

    if (scale == None):
        obj.setScale(scaleX, 1, scaleY)
    else:
        obj.setScale(scale)

    obj.setBin("unsorted", 0) # ignore draw order (z-fighting fix)       
    obj.setDepthTest(True)   # Don't disable depth write like the tut says

    if transparency:
        obj.setTransparency(1) #All of our objects are transparent
    if tex:
        tex = app.loader.loadTexture("textures/"+tex+".png") #Load the texture
        tex.setWrapU(Texture.WMClamp)                    # default is repeat, which will give
        tex.setWrapV(Texture.WMClamp)                    # artifacts at the edges
        obj.setTexture(tex, 1)                           #Set the texture

    return obj
