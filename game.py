import sfml as sf
import os

def main():
    desktop_mode = sf.VideoMode.get_desktop_mode()
    
    window = sf.RenderWindow(sf.VideoMode(800,600), 'GameTest')

    window.framerate_limit = 60
    fullscreen = False
    running = True

    inconsolata = sf.Font.load_from_file(os.path.join(os.path.dirname(__file__), 'data', 'fonts','ttf-inconsolata.otf'))
    fps_text = sf.Text('FPS: 0', inconsolata, 18)
    fps_text.color = sf.Color.WHITE
    fps_text.x = 4
    fps_text.y = 0

    fps_clock = sf.Clock()

    while running:
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Keyboard.ESCAPE:
                    """ Exit Game on Escape """
                    running = False

                if event.code == sf.Keyboard.F11:
                    """ Toggle Fullscreen on F11 """
                    if fullscreen:
                        window.create(sf.VideoMode(800, 600), 
                                    'GameTest', 
                                    sf.Style.DEFAULT)
                
                    if not fullscreen:
                        window.create(desktop_mode,
                                    'GameTest',
                                    sf.Style.FULLSCREEN)

                    fullscreen = not fullscreen

        fps = 1 / (fps_clock.elapsed_time.as_seconds())
        fps_clock.restart()

        fps_text.string = u'FPS: %i' % (fps)
        
        window.clear(sf.Color(94,94,94))
        window.draw(fps_text)
        window.display()

    window.close()

if __name__ == '__main__':
    main()
