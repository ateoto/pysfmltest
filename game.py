import sfml as sf
import os
import logging
import asyncore

from ui import UI

from chat_client import ChatClient

def main():
    desktop_mode = sf.VideoMode.get_desktop_mode()
    
    window = sf.RenderWindow(sf.VideoMode(800,600), 'GameTest')

    window.framerate_limit = 61
    fullscreen = False
    running = True

    fps_clock = sf.Clock()

    logging.basicConfig(level=logging.INFO)

    ui = UI(window)
    chat = ChatClient('Ateoto', ui)

    while running:
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False
            
            elif event.type == sf.Event.TEXT_ENTERED and chat.capturing_text:
                if event.unicode <> '\b':
                    chat.buffer += event.unicode

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Keyboard.ESCAPE:
                    """ Exit Game on Escape """
                    running = False

                if event.code == sf.Keyboard.BACK_SPACE and chat.capturing_text:
                    chat.buffer = chat.buffer[:-1]

                if event.code == sf.Keyboard.T and not chat.capturing_text or event.code == sf.Keyboard.RETURN and not chat.capturing_text:
                    chat.buffer = ''
                    chat.capturing_text = True
                    ui.chat_buffer.visible = True
                    break

                if event.code == sf.Keyboard.RETURN and chat.capturing_text:
                    if len(chat.buffer[1:]) >= 1:
                        chat.say(chat.buffer[1:])
                    chat.buffer = ''
                    chat.capturing_text = False
                    ui.chat_buffer.visible = False

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

        ui.fps.drawable.string = u'FPS: %i' % (fps)
        ui.chat_buffer.drawable.string = u':%s' % chat.buffer[1:]
        chat.tick(window.iter_events())

        window.clear(sf.Color(94,94,94))
        ui.draw()
        window.display()

    window.close()

if __name__ == '__main__':
    main()
