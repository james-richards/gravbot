from direct.showbase.ShowBase import ShowBase
from mainmenu import MainMenu

class App(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		
		self.screens = []
		self.screens.append(MainMenu(self))

	def run(self):
		# start first screen
		self.screens[-1].enter()

		ShowBase.run(self)



myApp = App()
myApp.run()
