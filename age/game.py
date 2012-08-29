import sfml as sf
from age.clock import GameClock
from age.ui import UI

class Game(object):
    def __init__(self, title):
        self.clock = GameClock()
        self.window = sf.RenderWindow(sf.VideoMode(800, 600), title)
        self.running = False
        self.player_character = None
        self.level = None
        self.ui = UI(sf.Vector2f(self.window.width, self.window.height))

    def update(self, dt):
        pass

    def handle_input(self, dt):
        for event in self.window.iter_events():
            if event.type == sf.Event.CLOSED:
                self.running = False

            if event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Keyboard.ESCAPE:
                    self.running = False

                if self.player_character:
                    self.player_character.handle_input(event, dt)

    def run(self):
        self.running = True

        # Update the Clock every second
        self.clock.schedule_interval(self.clock.calculate_fps, 1)

        while self.running:
            delta_time = self.clock.update()
            self.handle_input(delta_time.as_seconds())
            self.update(delta_time.as_seconds())
            #print(self.clock.fps)

            self.window.clear(sf.Color(94, 94, 94))
            if self.level is not None:
                self.window.draw(self.level)
            self.window.display()
