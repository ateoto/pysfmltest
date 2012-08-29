from xml.etree import ElementTree

import sfml as sf

from base64 import b64decode
import StringIO
import gzip
import struct
import time

import os

class TiledTile(sf.Sprite):
    def __init__(self, gid, texture):
        super(TiledTile, self).__init__(texture)
        self.gid = gid

class TiledCell(sf.Sprite):
    def __init__(self, pos, tile):
        self.tile = tile
        super(TiledCell, self).__init__(self.tile.texture)
        self.position = pos

    def draw(self, target, states):
        target.draw(self)

    def __repr__(self):
        return u'(%s, %s)' % (self.position[0], self.position[1])

class TiledLayerIterator:
    def __init__(self, layer):
        self.layer = layer
        self.i, self.j = 0, 0
    def next(self):
        if self.i == self.layer.rows:
            self.j += 1
            self.i = 0
        if self.j == self.layer.columns:
            raise StopIteration()
        value = self.layer[self.i, self.j]
        self.i += 1

        return value

class TiledLayer(sf.Sprite):
    def __init__(self, rows, columns):
        super(TiledLayer, self).__init__()
        self.cells = {}
        self.rows = rows
        self.columns = columns
        self.visible = True

    def __iter__(self):
        return TiledLayerIterator(self)

    def __getitem__(self, pos):
        return self.cells.get(pos)

class TiledTileset:
    def __init__(self, first_gid, image):
        self.first_gid = first_gid
        self.image = sf.Image.load_from_file(image)
        self.tiles = {}
        local_id = 0
        for y in range(0, self.image.height / 32):
            for x in range(0, self.image.width / 32):
                global_id = int(self.first_gid) + local_id
                area = sf.IntRect(x * 32, y * 32, 32, 32)
                tile_texture = sf.Texture.load_from_image(self.image, area)
                self.tiles.update({global_id : TiledTile(global_id, tile_texture)})
                local_id += 1


class TiledMap:
    def __init__(self, filename, area = None):
        self.layers = []
        self.tiles = {}
        self.area = area
        self.load_started = time.time()
        self.load_from_file(filename)

    def load_from_file(self, filename):
        tree = ElementTree.parse(filename)
        root = tree.getroot()

        map_dir = os.path.dirname(filename)

        self.width = int(root.attrib.get('width'))
        self.height = int(root.attrib.get('height'))
        self.tilewidth = int(root.attrib.get('tilewidth'))
        self.tileheight = int(root.attrib.get('tileheight'))
        self.pixel_width = int(self.width * self.tilewidth)
        self.pixel_height = int(self.height * self.tileheight)

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
            tl = TiledLayer(self.width, self.height)
            tl.name = layer.attrib.get('name')
            if tl.name == 'collision':
                tl.visible = False

            data = layer.find('data').text.rstrip().lstrip()
            data = b64decode(data)
            data = gzip.GzipFile(fileobj=StringIO.StringIO(data))
            data = data.read()
            data = struct.unpack('<%di' % (len(data)/4,), data)
            cell_num = 1
            for i, gid in enumerate(data):
                if gid < 1: continue
                x = i  % self.width
                y = i // self.width
 
                if gid in self.tiles.keys():
                    tl.cells[x,y] = TiledCell((x * 32, y * 32), self.tiles[gid])
                    cell_num +=1

            rt = sf.RenderTexture(self.pixel_width, self.pixel_height)
            rt.clear(sf.Color.TRANSPARENT)
            draw_count = 0
            for cell in tl:
                if cell is not None:
                    draw_count += 1
                    rt.draw(cell)
            if draw_count == len(tl.cells): pass
            rt.display()
            tl.set_texture(sf.Texture.load_from_image(rt.texture.copy_to_image()))       
            self.layers.append(tl)
        self.load_finished = time.time()
        load_time = self.load_finished - self.load_started
        print load_time

    def draw(self, target, states):
        for layer in self.layers:
            if layer.visible:
                target.draw(layer)
