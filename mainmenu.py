from gamescreen import GameScreen
from explorescreen import ExploreScreen
from panda3d.rocket import LoadFontFace, RocketRegion, RocketInputHandler

class MainMenu(GameScreen):

	def __init__(self, app):
		GameScreen.__init__(self, app)

		LoadFontFace("menus/Delicious-Roman.otf")

		self.region = RocketRegion.make('pandaRocket', self.app.win)
		self.region.setActive(1)
		context = self.region.getContext()

		self.menu = context.LoadDocument('menus/main_menu.rml')
		self.menu.hook = self

	def enter(self):
		self.menu.Show()

		ih = RocketInputHandler()
		self.app.mouseWatcher.attachNewNode(ih)
		self.region.setInputHandler(ih)

	def exit(self):
		self.region.setActive(0)
		self.menu.Close()

	def pause(self):
		self.region.setActive(0)

	def resume(self):
		self.region.setActive(1)

	def loadMenu(self, opt):
		print "hello menu " + opt

	def startExplore(self):
		self.app.screens.append(ExploreScreen(self.app))
		self.exit()
		self.app.screens[-1].enter()
