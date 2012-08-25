import sfml as sf

class AnimatedSprite(sf.Sprite):

    def draw(self, target, states):
        target.draw(self.texture)
    
    def animate(self, animation):
        pass

