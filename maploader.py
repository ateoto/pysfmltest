import os
from base64 import b64decode
import gzip
import StringIO
from xml.dom.minidom import parse

tiled = parse(os.path.join('data','maps','test.tmx'))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

for layer in tiled.getElementsByTagName('layer'):
    print layer.attributes['name'].value
    data = layer.firstChild
    print data.data
