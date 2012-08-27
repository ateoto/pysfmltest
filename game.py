import sfml as sf
import os
import logging
import asyncore

import age

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

    game_clock = sf.Clock()

    fps_clock = sf.Clock()

    logging.basicConfig(level=logging.INFO)

    ui = UI(window)
    chat = ChatClient('Ateoto', ui)
    

    wc_base_t = sf.Texture.load_from_file('data/actors/human_male/walkcycle/BODY_animation.png')
    wc_t = sf.RenderTexture(wc_base_t.width, wc_base_t.height)
    wc_t.clear(sf.Color.TRANSPARENT)

    wc_base = sf.Sprite(wc_base_t)
    wc_armor = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/TORSO_leather_armor_torso.png'))
    wc_shoulders = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/TORSO_leather_armor_shoulders.png'))
    wc_bracers = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/TORSO_leather_armor_bracers.png'))
    wc_hair = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/HEAD_hair_blonde.png'))
    wc_pants = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/LEGS_pants_greenish.png'))
    wc_boots = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/walkcycle/FEET_shoes_brown.png'))

    wc_t.draw(wc_base)
    wc_t.draw(wc_hair)
    wc_t.draw(wc_armor)
    wc_t.draw(wc_pants)
    wc_t.draw(wc_shoulders)
    wc_t.draw(wc_bracers)
    wc_t.draw(wc_boots)

    wc_t.display()
    
    walkcycle_north_frames = deque()
    walkcycle_south_frames = deque()
    walkcycle_east_frames = deque()
    walkcycle_west_frames = deque()


    for f in range(0, wc_t.width, 64):
        walkcycle_north_frames.append(AnimationFrame(wc_t.texture, sf.IntRect(f, 0, 64, 64), 0.1))
        walkcycle_south_frames.append(AnimationFrame(wc_t.texture, sf.IntRect(f, 128, 64, 64), 0.1))
        walkcycle_east_frames.append(AnimationFrame(wc_t.texture, sf.IntRect(f, 64, 64, 64), 0.1))
        walkcycle_west_frames.append(AnimationFrame(wc_t.texture, sf.IntRect(f, 192, 64, 64), 0.1))


    walkcycle_north = Animation(walkcycle_north_frames)
    walkcycle_south = Animation(walkcycle_south_frames)
    walkcycle_east = Animation(walkcycle_east_frames)
    walkcycle_west = Animation(walkcycle_west_frames)

    s_base_t = sf.Texture.load_from_file('data/actors/human_male/slash/BODY_animation.png')
    s_t = sf.RenderTexture(s_base_t.width, s_base_t.height)
    s_t.clear(sf.Color.TRANSPARENT)

    s_base = sf.Sprite(s_base_t)
    s_armor = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/TORSO_leather_armor_torso.png'))
    s_shoulders = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/TORSO_leather_armor_shoulders.png'))
    s_bracers = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/TORSO_leather_armor_bracers.png'))
    s_hair = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/HEAD_hair_blonde.png'))
    s_pants = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/LEGS_pants_greenish.png'))
    s_boots = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/FEET_shoes_brown.png'))
    s_dagger = sf.Sprite(sf.Texture.load_from_file('data/actors/human_male/slash/WEAPON_dagger.png'))

    s_t.draw(s_base)
    s_t.draw(s_hair)
    s_t.draw(s_armor)
    s_t.draw(s_pants)
    s_t.draw(s_shoulders)
    s_t.draw(s_bracers)
    s_t.draw(s_boots)
    s_t.draw(s_dagger)

    s_t.display()

    s_north_frames = deque()
    s_south_frames = deque()
    s_east_frames = deque()
    s_west_frames = deque()

    for f in range(0, s_t.width, 64):
        s_north_frames.append(AnimationFrame(s_t.texture, sf.IntRect(f, 0, 64, 64), 0.05))
        s_south_frames.append(AnimationFrame(s_t.texture, sf.IntRect(f, 128, 64, 64), 0.05))
        s_east_frames.append(AnimationFrame(s_t.texture, sf.IntRect(f, 64, 64, 64), 0.05))
        s_west_frames.append(AnimationFrame(s_t.texture, sf.IntRect(f, 192, 64, 64), 0.05))
        

    s_north = Animation(s_north_frames)
    s_south = Animation(s_south_frames)
    s_east = Animation(s_east_frames)
    s_west = Animation(s_west_frames)

    s_anims = [ s_north, s_east, s_south, s_west ]

    me = AnimatedSprite(wc_t.texture)
    me.set_texture_rect(sf.IntRect(0, 128, 64, 64))

    me.position = (window.width / 2, window.height / 2)
    
    facing = 2


    map = age.map.TiledMap('data/maps/0_0.tmx')

    while running:
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False
            
            elif event.type == sf.Event.TEXT_ENTERED and chat.capturing_text:
                if event.unicode <> '\b':
                    chat.buffer += event.unicode

            elif event.type == sf.Event.KEY_PRESSED:
                """
                if event.code == sf.Keyboard.W:
                    me.animate(walkcycle_north, loop = True)

                if event.code == sf.Keyboard.S:
                    me.animate(walkcycle_south, loop = True)
                
                if event.code == sf.Keyboard.A:
                    me.animate(walkcycle_east, loop = True)

                if event.code == sf.Keyboard.D:
                    me.animate(walkcycle_west, loop = True)
                """
    
                if event.code == sf.Keyboard.NUM1:
                    me.animate(s_anims[facing])

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

        if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            if not me.is_animating or me.animation is not walkcycle_north: 
                me.animate(walkcycle_north, loop=True)
            facing = 0
            me.move(0,-2)
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.A):
            if not me.is_animating or me.animation is not walkcycle_east:
                me.animate(walkcycle_east, loop=True)
            facing = 1
            me.move(-2, 0)
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            if not me.is_animating or me.animation is not walkcycle_south:
                me.animate(walkcycle_south, loop=True)
            facing = 2
            me.move(0,2)
        elif sf.Keyboard.is_key_pressed(sf.Keyboard.D):
            if not me.is_animating or me.animation is not walkcycle_west:
                me.animate(walkcycle_west, loop=True)
            facing = 3
            me.move(2,0)
        else:
            if me.is_animating: 
                if me.animation not in [s_north, s_south, s_east, s_west]:
                    me.stop_animation()

        fps = 1 / (fps_clock.elapsed_time.as_seconds())
        delta_time = fps_clock.restart()

        ui.fps.drawable.string = u'FPS: %i' % (fps)
        ui.chat_buffer.drawable.string = u':%s' % chat.buffer[1:]
        chat.tick(window.iter_events())

        me.update(delta_time.as_seconds())

        window.clear(sf.Color(94,94,94))
        window.draw(map)
        window.draw(me)
        ui.draw()
        window.display()

    window.close()

if __name__ == '__main__':
    main()
