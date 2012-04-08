from direct.showbase.ShowBase import ShowBase
from panda3d.rocket import *

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)

app = MyApp()
app.run()
