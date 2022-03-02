from parse import Parse as p
from convert import Convert

from node import TextDraw, LineDraw, settings


from PIL import Image
import os


def fresh(cfg = settings): # get new image w/ default size etc
    return Image.new("RGBA",(cfg["W"], cfg["H"]), cfg["bg_color"]) # random


# image = fresh()

sample = """[IP
   [NP 
        [DP [D the] [D 30]]
        [N'
            <AdjP very big>
            [N dogs]]]
   [I'
        [I will]
        [VP [V be] [P here]]]]"""

outdir = "out/"
sample_file = "default.png"
outfile = "out.png"

settings['sentence'] = sample
settings['default_file'] = sample_file
settings['output_dir'] = outdir
settings['output_file'] = outdir + outfile
settings['reparse?'] = True

def create_tree (s): # this is the only one that SHOULDNT need cfg!
    pr = p.parse(s)
    tree = Convert(parse_results = pr).to_tree()
    return tree


def draw_tree (tree, cfg = settings):
    # print(f"This tree has {tree.all_terminal_children_count} terminal children")
    i = fresh(cfg)
    tree.draw_node(i, cfg)
    return i

def save_tree (tree, filename = outfile, cfg = settings):
    i = draw_tree(tree, cfg)
    i.save(filename)
    return i
    # return filename

