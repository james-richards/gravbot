import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.directbase import DirectStart

from panda3d.rocket import *

LoadFontFace("menus/Delicious-Roman.otf")

r = RocketRegion.make('pandaRocket', base.win)
r.setActive(1)
context = r.getContext()

menu = context.LoadDocument('menus/main_menu.rml')
menu.Show()

ih = RocketInputHandler()
base.mouseWatcher.attachNewNode(ih)
r.setInputHandler(ih)


run()

