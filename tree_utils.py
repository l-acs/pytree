from parse import Parse as p
from convert import Convert

from node import TextDraw, LineDraw, line_height, default_width, margin, padding


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

sample_file = "default.png"
outfile = "out.png"

def create_tree (s):
    pr = p.parse(s)
    tree = Convert(parse_results = pr).to_tree()
    return tree


def draw_tree (tree, width = default_width):
    i = fresh()
    tree.draw_node(i, coord, width)
    return i

def save_tree (tree, filename = outfile, width = default_width):
    i = draw_tree(tree, width)
    i.save(filename)
    return i
    # return filename

def show_tree (tree, width = default_width):
    # not useful. for testing
    i = draw_tree(tree, width)
    i.show()



