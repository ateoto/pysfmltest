import sfml as sf
import os

class Element(object):
    def __init__(self):
        self.visible = True
        self.drawable = None

    def draw(self, window):
        if self.visible and self.drawable:
            window.draw(self.drawable)

class TextElement(Element):
    def __init__(self, string, font, size, pos):
        super(TextElement, self).__init__()
        self.font = font
        self.string = string
        self.size = size
        self.drawable = sf.Text(self.string, self.font, self.size)
        self.drawable.position = pos

class UI(object):
    def __init__(self, window):
        self.window = window

        self.fonts = {
            'inconsolata' : sf.Font.load_from_file(os.path.join(os.path.dirname(__file__), 'data', 'fonts','ttf-inconsolata.otf'))
        }

        self.fps = TextElement('', self.fonts['inconsolata'], 18, (0,0))
        self.chat_log = TextElement('', self.fonts['inconsolata'], 18, (30, 30))
        self.chat_buffer = TextElement('', self.fonts['inconsolata'], 18, (0, self.window.height - 20))
        self.chat_buffer.visible = False

        self.drawables = []
        self.drawables.append(self.chat_log)
        self.drawables.append(self.chat_buffer) 
        self.drawables.append(self.fps)

    def draw(self):
        for drawable in self.drawables:
            drawable.draw(self.window)
