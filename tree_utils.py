import re
from parse import Parse as p
from convert import Convert

from node import TextDraw, LineDraw, settings

import streamlit as st
from PIL import Image
import os

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
settings['reload_tree?'] = True # true for the first run!

blank_regexp = re.compile(r'\s+')

def reorder_insert_at_top(l, elem): # for fonts
    t = l.copy()
    t.sort()

    if elem in t:
        t.remove(elem)

    t.insert(0, elem)
    return t

@st.experimental_memo(persist="disk") # probably overkill
def sanity_check (sentence):
    return (sentence and blank_regexp.sub('', sentence) != '')

@st.experimental_memo(persist="disk")
def fresh (width, height, bg_color):
    return Image.new("RGBA", (width, height), bg_color)


@st.experimental_memo(persist="disk")
def create_tree (s):
    # print('reparsing')
    pr = p.parse(s)
    tree = Convert(parse_results = pr).to_tree()
    return tree

def draw_tree (tree, cfg = settings):
    i = fresh(cfg['W'], cfg['H'], cfg['bg_color'])
    tree.draw_node(i, cfg)
    return i

def save_tree (tree, filename = outfile, cfg = settings):
    i = draw_tree(tree, cfg)
    i.save(filename)
    return i
