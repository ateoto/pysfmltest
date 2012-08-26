import sfml as sf
from collections import deque



"""
texture = sf.Texture.load_from_file('data/art/male_walkcycle.png')


frames = deque()

for f in range(0, texture.width, 64):
    frames.append(AnimationFrame(texture, sf.IntRect(0,f,64,64), 0.1)


walkcycle_north = Animation([
                    AnimationFrame(texture, sf.IntRect(0,0,64,64), 0.1),
                    AnimationFrame(texture, sf.IntRect(0,64,64,64), 0.1),
                    AnimationFrame(texture, sf.IntRect(0,128,64,64), 0.1)])

pc = AnimatedSprite(texture)
pc.set_texture_rect(sf.IntRect(0,0,64,64)) # Sets North facing

pc.animate(walkcycle_north)
pc.update(delta_time)
window.draw(pc)
pc.stop_animation()


"""

class AnimationFrame(object):
    def __init__(self, texture, area, duration):
        self.texture = texture
        self.area = area
        self.duration = duration

class Animation(object):
    def __init__(self, frames):
        if isinstance(frames, list):
            self.frames = deque()
            for f in frames:
                self.frames.append(f)
        elif isinstance(frames, deque):
            self.frames = frames
        else:
            raise TypeError('frames must be a deque or list')


class AnimatedSprite(sf.Sprite):
    def __init__(self, texture):
        super(AnimatedSprite, self).__init__(texture)
        self.is_animating = False

    def animate(self, animation, loop = False):
        self.is_animating = True
        self.loop = loop
        self.animation = animation
        self.frame_index = 0
        self.set_texture(self.animation.frames[self.frame_index].texture)
        self.set_texture_rect(self.animation.frames[self.frame_index].area)
        self.next_dt = 0


    def stop_animation(self):
        self.is_animating = False
        self.set_texture(self.animation.frames[0].texture)
        self.set_texture_rect(self.animation.frames[0].area)

    def update(self, delta_time):
        if self.is_animating:
            self.next_dt += delta_time
            if self.next_dt >= self.animation.frames[self.frame_index].duration:
                if self.frame_index + 1 <= len(self.animation.frames) - 1:
                    self.frame_index += 1
                    self.set_texture(self.animation.frames[self.frame_index].texture)
                    self.set_texture_rect(self.animation.frames[self.frame_index].area)
                    self.next_dt = 0
                else:
                    if self.loop:
                        self.animate(self.animation, loop = True)
                    else:
                        self.is_animating = False
                        self.set_texture(self.animation.frames[0].texture)
                        self.set_texture_rect(self.animation.frames[0].area)

    def draw(self, target, states):
        target.draw(self)
