import sfml as sf
import os
import logging
import asyncore

from chat_client import Client

def main():
    desktop_mode = sf.VideoMode.get_desktop_mode()
    
    window = sf.RenderWindow(sf.VideoMode(800,600), 'GameTest')

    window.framerate_limit = 61
    fullscreen = False
    running = True

    inconsolata = sf.Font.load_from_file(os.path.join(os.path.dirname(__file__), 'data', 'fonts','ttf-inconsolata.otf'))
    fps_text = sf.Text('FPS: 0', inconsolata, 18)
    fps_text.color = sf.Color.WHITE
    fps_text.x = 4
    fps_text.y = 0

    chat_buffer = sf.Text(u'', inconsolata, 18)

    chat_buffer.x = 0
    chat_buffer.y = window.height - 20

    fps_clock = sf.Clock()

    buffer = ''
    capture_text = False

    logging.basicConfig(level=logging.INFO)

    c = Client(('127.0.0.1', 9999), 'Ateoto')

    while running:
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False
            
            elif event.type == sf.Event.TEXT_ENTERED and capture_text:
                if event.unicode <> '\b':
                    buffer += event.unicode

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Keyboard.ESCAPE:
                    """ Exit Game on Escape """
                    running = False

                if event.code == sf.Keyboard.BACK_SPACE and capture_text:
                    buffer = buffer[:-1]

                if event.code == sf.Keyboard.T and not capture_text or event.code == sf.Keyboard.RETURN and not capture_text:
                    buffer = ''
                    capture_text = True
                    break

                if event.code == sf.Keyboard.RETURN and capture_text:
                    if len(buffer[1:]) >= 1:
                        c.say(buffer[1:])
                    buffer = ''
                    capture_text = False

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
    
        chat_buffer.string = u':%s' % buffer[1:]

        asyncore.loop(count=1)

        window.clear(sf.Color(94,94,94))
        window.draw(fps_text)
        if capture_text:
            window.draw(chat_buffer)
        window.display()

    window.close()

if __name__ == '__main__':
    main()
