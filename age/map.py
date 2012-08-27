from xml.etree import ElementTree

import sfml as sf

from base64 import b64decode
import StringIO
import gzip
import struct

import os

class TiledTile(object):
    def __init__(self, gid, texture, area):
        self.gid = gid
        self.texture = texture
        self.area = area
        print self.area

class TiledCell(sf.Sprite):
    def __init__(self, pos, tile):
        super(TiledCell, self).__init__(tile.texture)
        self.set_texture_rect(tile.area)
        self.position = pos

    def __repr__(self):
        return u'%s:%s' % (self.texture, self.position)

class TiledLayerIterator:
    def __init__(self, layer):
        self.layer = layer
        self.i, self.j = 0, 0
    def next(self):
        if self.i == self.layer.width - 1:
            self.j += 1
            self.i = 0
        if self.j == self.layer.height - 1:
            raise StopIteration()
        value = self.layer[self.i, self.j]
        self.i += 1

        return value

class TiledLayer:
    def __init__(self):
        self.name = ''
        self.height = 100
        self.width = 100
        self.cells = {}

    def __iter__(self):
        return TiledLayerIterator(self)

    def __getitem__(self, pos):
        return self.cells.get(pos)

class TiledTileset:
    def __init__(self, first_gid, image):
        self.first_gid = first_gid
        self.texture = sf.Texture.load_from_file(image)
        self.tiles = {}
        print self.texture.height
        local_id = 0
        for y in range(0, self.texture.height / 32 + 1):
            for x in range(0, self.texture.width / 32 + 1):
                global_id = int(self.first_gid) + local_id
                area = sf.IntRect(x * 32, y * 32, 32, 32)
                self.tiles.update({global_id : TiledTile(global_id, self.texture, area)})
                local_id += 1

class TiledMap:
    def __init__(self, filename):
        self.layers = []
        self.tiles = {}
        self.load_from_file(filename)

    def load_from_file(self, filename):
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        map_dir = os.path.dirname(filename)

        # Need to load tilesets.
        for tileset in root.findall('tileset'):
            firstgid = tileset.attrib.get('firstgid')
            source = tileset.attrib.get('source')
            tileset_file = os.path.join(map_dir, source)
            ts_tree = ElementTree.parse(os.path.join(map_dir, source))
            ts_root = ts_tree.getroot()
            image = ts_root.findall('image')[0].attrib.get('source')
            image = os.path.join(map_dir, image)
            ts = TiledTileset(firstgid, image)
            self.tiles.update(ts.tiles)

        for layer in root.findall('layer'):
            tl = TiledLayer()
            tl.name = layer.attrib.get('name')

            data = layer.find('data').text.rstrip().lstrip()
            data = b64decode(data)
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data))
            data = data.read()
            data = struct.unpack('<%di' % (len(data)/4,), data)
            for i, gid in enumerate(data):
                if gid < 1: continue
                x = i  % 100
                y = i // 100
        
                if gid in self.tiles.keys():
                    tl.cells[x,y] = TiledCell((x * 32, y * 32), self.tiles[gid])

            self.layers.append(tl)

    def draw(self, target, states):
        for layer in self.layers:
            for cell in layer:
                if cell:
                    target.draw(cell)
                


