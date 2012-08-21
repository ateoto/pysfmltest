import sfml as sf

def main():
    desktop_mode = sf.VideoMode.get_desktop_mode()
    
    window = sf.RenderWindow(sf.VideoMode(800,600), 'GameTest')

    window.framerate_limit = 60
    fullscreen = False
    running = True

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

        window.clear(sf.Color(94,94,94))
        window.display()

    window.close()

if __name__ == '__main__':
    main()
