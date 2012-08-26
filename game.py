import sfml as sf
import os
import logging
import asyncore

from collections import deque

from ui import UI
from animatedsprite import AnimationFrame, Animation, AnimatedSprite

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
    

    walkcycle_texture = sf.Texture.load_from_file('data/art/male_walkcycle.png')

    walkcycle_with_clothes = sf.RenderTexture(walkcycle_texture.width, walkcycle_texture.height)

    walkcycle_with_clothes.clear(sf.Color.TRANSPARENT)


    base_me = sf.Sprite(walkcycle_texture)
    armor = sf.Sprite(sf.Texture.load_from_file('data/art/lpc_entry/png/walkcycle/TORSO_leather_armor_torso.png'))
    shoulders = sf.Sprite(sf.Texture.load_from_file('data/art/lpc_entry/png/walkcycle/TORSO_leather_armor_shoulders.png'))
    bracers = sf.Sprite(sf.Texture.load_from_file('data/art/lpc_entry/png/walkcycle/TORSO_leather_armor_bracers.png'))
    pants = sf.Sprite(sf.Texture.load_from_file('data/art/lpc_entry/png/walkcycle/LEGS_pants_greenish.png'))
    boots = sf.Sprite(sf.Texture.load_from_file('data/art/lpc_entry/png/walkcycle/FEET_shoes_brown.png'))

    walkcycle_with_clothes.draw(base_me)
    walkcycle_with_clothes.draw(armor)
    walkcycle_with_clothes.draw(pants)
    walkcycle_with_clothes.draw(shoulders)
    walkcycle_with_clothes.draw(bracers)
    walkcycle_with_clothes.draw(boots)

    walkcycle_with_clothes.display()
    walkcycle_clothes_texture = walkcycle_with_clothes.texture
    walkcycle_north_frames = deque()
    walkcycle_south_frames = deque()
    walkcycle_east_frames = deque()
    walkcycle_west_frames = deque()


    for f in range(0, walkcycle_texture.width, 64):
        walkcycle_north_frames.append(AnimationFrame(walkcycle_clothes_texture, sf.IntRect(f, 0, 64, 64), 0.1))
        walkcycle_south_frames.append(AnimationFrame(walkcycle_clothes_texture, sf.IntRect(f, 128, 64, 64), 0.1))
        walkcycle_east_frames.append(AnimationFrame(walkcycle_clothes_texture, sf.IntRect(f, 64, 64, 64), 0.1))
        walkcycle_west_frames.append(AnimationFrame(walkcycle_clothes_texture, sf.IntRect(f, 192, 64, 64), 0.1))


    walkcycle_north = Animation(walkcycle_north_frames)
    walkcycle_south = Animation(walkcycle_south_frames)
    walkcycle_east = Animation(walkcycle_east_frames)
    walkcycle_west = Animation(walkcycle_west_frames)

    me = AnimatedSprite(sf.Texture.load_from_file('data/art/male_walkcycle.png'))
    me.set_texture_rect(sf.IntRect(0, 128, 64, 64))

    me.position = (window.width / 2, window.height / 2)

    while running:
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False
            
            elif event.type == sf.Event.TEXT_ENTERED and chat.capturing_text:
                if event.unicode <> '\b':
                    chat.buffer += event.unicode

            elif event.type == sf.Event.KEY_PRESSED:
                if event.code == sf.Keyboard.W:
                    me.animate(walkcycle_north, loop = True)

                if event.code == sf.Keyboard.S:
                    me.animate(walkcycle_south, loop = True)
                
                if event.code == sf.Keyboard.A:
                    me.animate(walkcycle_east, loop = True)

                if event.code == sf.Keyboard.D:
                    me.animate(walkcycle_west, loop = True)

                if event.code == sf.Keyboard.Q:
                    me.stop_animation()

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
        delta_time = fps_clock.restart()

        ui.fps.drawable.string = u'FPS: %i' % (fps)
        ui.chat_buffer.drawable.string = u':%s' % chat.buffer[1:]
        chat.tick(window.iter_events())

        me.update(delta_time.as_seconds())

        window.clear(sf.Color(94,94,94))
        window.draw(me)
        ui.draw()
        window.display()

    window.close()

if __name__ == '__main__':
    main()
