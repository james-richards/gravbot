from entity import Entity

class LightLaserShot(Entity):
  speed = 1.0

  def __init__(self, pos, vel):
    super(LightLaserShot, self).__init__()

    self.pos = pos
    self.vel = vel

  def update(self, timer):
    self.pos = self.pos + timer * self.vel 

