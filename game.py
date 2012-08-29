import age
import sfml as sf
import logging as log

log.basicConfig(level=log.DEBUG)

g = age.game.Game('My Game')

area = sf.IntRect(0,0,g.window.width, g.window.height)

g.load_map('data/maps/0_0.tmx', area)
g.player_character = age.actor.PCActor(g.level.objects['pc_initial_spawn'].position)
g.player_character.sprite.set_texture_rect(sf.IntRect(0, 128, 64, 64))

g.run()
