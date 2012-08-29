import age
import sfml as sf

g = age.game.Game('My Game')

area = sf.IntRect(0,0,g.window.width, g.window.height)
tm = age.map.TiledMap('data/maps/0_0.tmx', area)

g.level = tm
g.player_character = age.actor.PCActor(sf.Vector2f(0,0))
g.run()
