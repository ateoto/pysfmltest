from xml.etree import ElementTree

from base64 import b64decode
import StringIO
import gzip
import struct



class TiledTile:


class TiledCell:
    def __init__(self, x, y, px, py, tile):
        self.x = px
        self.y = py
        self.px = px
        self.py = py
        self.tile = tile

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
    pass

class TiledMap:
    def __init__(self, filename):
        self.layers = list()
        self.load_from_file(filename)

    def load_from_file(self, filename):
        tree = ElementTree.parse(filename)
        root = tree.getroot()
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
                tl.cells[x,y] = TiledCell(x, y, x * 32, y * 32, gid)

            self.layers.append(tl)
