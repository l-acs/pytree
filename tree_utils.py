import sys
# temporarily
sys.path.append("/home/l-acs/projects/python/pytree")
from parse import Parse as p
from convert import Convert

from PIL import Image
import os


W, H = 2500, 1000
coord = (W/2, 50)

def fresh(): # get new image w/ default size etc
    return Image.new("RGBA",(W,H),"white") # random


image = fresh()

sample = """[IP
   [NP 
        [DP [D the] [D 30]]
        [N'
            [AdjP very big]
            [N dogs]]]
   [I'
        [I will]
        [VP [V be] [P here]]]]"""

outfile = "out.png"


def create_tree (s):
    pr = p.parse(s)
    tree = Convert(parse_results = pr).to_tree()
    return tree


def draw_tree (tree):
    i = fresh()
    tree.draw_node(i, coord)
    return i

def save_tree (tree, filename = outfile):
    i = draw_tree(tree)
    i.save(filename)
    return i
    # return filename

def show_tree (tree):
    # not useful. for testing
    i = draw_tree(tree)
    i.show()



