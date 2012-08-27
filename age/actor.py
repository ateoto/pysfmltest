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
    def __init__(self):
        super(PCActor, self).__init__()
