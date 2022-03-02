import streamlit as st
import tree_utils as t
from parse import Parse as p
import os

def set_defaults_if_empty (cfg = st.session_state, defaults = t.settings):
    for k in defaults:
        if k not in cfg:
            cfg[k] = defaults[k]
    return cfg

def reorder_insert_at_top(l, elem):
    t = l.copy()
    t.sort()

    if elem in t:
        t.remove(elem)

    t.insert(0, elem)
    return t


def set_fonts_if_empty (cfg = st.session_state, loc = 'fonts/'):
    if 'fonts_avail' not in cfg:
        fonts = [font_file.split('.')[0] for font_file in os.listdir('fonts/')]
        fonts.sort()
        cfg['fonts_avail'] = fonts

    return cfg


def set_tree_container_if_not_exists ():
    if 'tree_container' not in st.session_state:
        st.session_state['tree_container'] = st.empty()


def parse (cfg = st.session_state):
    try:
        if 'sentence' in cfg:
            cfg['tree'] = t.create_tree(cfg['sentence'])
    except p.ParseError:
        st.warning("It looks like that's not a valid tree! Please edit your text and try again.")


def gen_tree_image (cfg = st.session_state, f = None):
    if f is None:
        f = cfg['output_file']

    if 'tree' in cfg:
        cfg['img'] = t.save_tree(cfg['tree'], f, cfg)


def reload_tree (cfg = st.session_state, default = False):
    cfg['tree_container'].image(cfg['img'])

def initial_draw (cfg = st.session_state, default = False):
    if 'tree_container' in cfg and 'img' in cfg:
        reload_tree(cfg, default)


# todo: similarly for re-parsing
def redraw_tree_if_requested (cfg = st.session_state, default = False, reparse = False):
    if 'reload_tree?' in st.session_state and st.session_state['reload_tree?']:
        # st.write('requested')

        if reparse: # this probably shouldn't go here?
            parse(cfg)

        gen_tree_image(cfg, f = cfg['default_file'] if default else cfg['output_file'])
        set_tree_container_if_not_exists()
        reload_tree(cfg, default)
        st.session_state['reload_tree?'] = False
    # else:
    #     st.write('not requested')


def slidewrap(cfield, label, minv, maxv, step = 5, format = '%i pixels', cfg = st.session_state):

    prev = cfg[cfield]
    out = st.slider(label = label,
                    value = prev,
                    min_value = minv,
                    max_value = maxv,
                    step = step,
                    format = format
    )

    if out and out != prev:
        cfg[cfield] = out
        st.experimental_rerun() # this is the key bit
        return True
    else:
        return False


def colorwrap(cfield, label, cfg = st.session_state):

    prev = cfg[cfield]
    out = st.color_picker(label = label,
                    value = prev
    )

    if out and out != prev:
        cfg[cfield] = out
        st.experimental_rerun() # this is the key bit
        return True
    else:
        return False

def colorwrap_cols (tups, cfg = st.session_state):
    cols = st.columns(len(tups))
    new_selection = False

    for pairing in tups:
        (cfield, label) = pairing
        col = cols.pop()
        with col:
            new_selection = new_selection or colorwrap(cfield, label, cfg)

    return new_selection




def dropdownwrap(cfield, label, options, cfg = st.session_state):

    prev = cfg[cfield]

    options_tweaked = reorder_insert_at_top(options, prev) # fixes [unwanted [font reset]] on update

    out = st.selectbox(label, options_tweaked)

    if out and out != prev:
        cfg[cfield] = out
        st.experimental_rerun() # this is the key bit
        return True
    else:
        return False



def show_configurations (cfg = st.session_state):
    color_tups = [("fg_color", 'Foreground color'),
                  ("bg_color", 'Background color')]

    with st.expander("Show advanced options"):
        l = [
            slidewrap('W', 'Width of the whole image', 350, 3500),
            slidewrap('H', 'Height of the whole image', 350, 3500),

            slidewrap('font_size', 'Font size of text', 12, 44, step = 1, format = '%i pt'),

            dropdownwrap('font_style', 'Text font', cfg['fonts_avail']),

            slidewrap('top_padding', 'Top padding between node and branches', 4, 40, step = 2),
            slidewrap('bottom_padding', 'Bottom padding between branches and nodes', 4, 40, step = 2),
            colorwrap_cols(color_tups),

            slidewrap('margin', 'Margins around the tree', 0, 125)
        ]

    for config in l: # if any of these have returned a truthy value, i.e. slidewrap has determined a change has been made,
        if config:
            return config # then show_configurations should return that truth value to tell the app to redraw the tree

    return False


def textbox (old, cfg = st.session_state):
    out = st.text_area(label = "Enter your tree here",
                       value = old,
                       height = len(st.session_state['sentence'].splitlines()) * 20)

    if out and 'sentence' in cfg and out != cfg['sentence']:
        cfg['sentence'] = out

    return out




def header (name, subtitle, author = '🥷', git_url = 'github.com'):
    st.set_page_config(
        page_title = subtitle,
        page_icon = '🌳',
        menu_items= {
            'About': f'# {name}\nA linguistic {subtitle.lower()} by {author}',
            'Get Help': f'https://{git_url}/{author}/{name}/issues', # this is stupid but fun
            'Report a bug': None
        },

    )

    st.title(name)
    st.header(f'{name}  —  {subtitle}')


def homepage ():
    set_defaults_if_empty()
    set_fonts_if_empty()

    previous_text = st.session_state['sentence']
    new_text = textbox(previous_text, st.session_state)

    if st.session_state['sentence']:
        st.session_state['reload_tree?'] = True

    if show_configurations():
        st.session_state['reload_tree?'] = True

    if new_text != previous_text:
        st.session_state['reload_tree?'] = True
        st.experimental_rerun()
        redraw_tree_if_requested(reparse = st.session_state['reparse?'])


    if st.session_state['reload_tree?']:
        redraw_tree_if_requested(reparse = st.session_state['reparse?']) # draw iff requested, but reparse only if the sentence has changed


header('pytree', 'Syntax Tree Generator', 'l-acs')
homepage()
