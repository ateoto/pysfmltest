import sfml as sf

class Actor(object):
    """
    Base Actor Class, all Actors should inherit from this
    """

    def __init__(self):
        pass

class VisibleActor(Actor):
    def __init__(self):
        super(VisibleActor, self).__init__()

class MoveableActor(VisibleActor):
    def __init__(self):
        super(MoveableActor, self).__init__()

class NPCActor(MoveableActor):
    def __init__(self):
        super(NPCActor, self).__init__()

class PCActor(MoveableActor):
    def __init__(self, location):
        super(PCActor, self).__init__()
        self.timescale = 1
        self.movespeed = 100
        self.location = location
        self.moving_codes = [ sf.Keyboard.W, sf.Keyboard.A, sf.Keyboard.S, sf.Keyboard.D ]
        self.directions = { 'NORTH' : sf.Vector2f(0, -1),
                            'EAST' : sf.Vector2f(1, 0),
                            'SOUTH' : sf.Vector2f(0, 1),
                            'WEST' : sf.Vector2f(-1, 0)}

    def handle_input(self, event, dt):
        if event.code in self.moving_codes:
            if event.code == sf.Keyboard.W:
                self.move(self.directions['NORTH'], dt)
            elif event.code == sf.Keyboard.A:
                self.move(self.directions['WEST'], dt)
            elif event.code == sf.Keyboard.S:
                self.move(self.directions['SOUTH'], dt)
            elif event.code == sf.Keyboard.D:
                self.move(self.directions['EAST'], dt)
        else:
            self.stop_animation()
        


    def animate(self, animation):
        raise NotImplementedError

    def stop_animation(self):
        pass

    def move(self, location_delta, dt):
        location_delta.x = location_delta.x * self.movespeed * self.timescale
        location_delta.y = location_delta.y * self.movespeed * self.timescale
        # Check for collisions here?
        self.location += location_delta

    def draw(self, target, states):
        pass
