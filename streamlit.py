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
        s = cfg['sentence']
        if t.sanity_check(s):
            cfg['tree'] = t.create_tree(s)
            return True

    except p.ParseError:
        st.warning("It looks like that's not a valid tree! Please edit your text and try again.")

    return False

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


def redraw_tree_if_requested (cfg = st.session_state, default = False):
    if 'reload_tree?' in cfg and cfg['reload_tree?']:

        if 'sentence' in cfg and cfg['sentence']:
            p = parse(cfg)
            if not (p): # failed parse
                return # exit

        gen_tree_image(cfg, f = cfg['default_file'] if default else cfg['output_file'])
        set_tree_container_if_not_exists()
        reload_tree(cfg, default)
        st.session_state['reload_tree?'] = False


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

def buttonswap(cfield1, cfield2, label, cfg = st.session_state):
    buttonswap_state = f'{cfield1}_{cfield2}_buttonswap' # unique id for this swap button
    if buttonswap_state not in cfg:
        cfg[buttonswap_state] = False

    if cfg[buttonswap_state]:
        return True

    cfg[buttonswap_state] = st.button(label = label)

    if cfg[buttonswap_state]:
        tmp = cfg[cfield1]
        cfg[cfield1] = cfg[cfield2]
        cfg[cfield2] = tmp
        cfg[buttonswap_state] = False
        st.experimental_rerun() # this is the key bit
        return True

    else:
        return False



def colorwrap_cols (fg_field = 'fg_color', bg_field = 'bg_color', cfg = st.session_state):
    new_selection = False
    swap_col, fg_col, bg_col = st.columns([10, 1, 4])

    with fg_col:
        new_selection = new_selection or colorwrap(fg_field, '', cfg)

    with bg_col:
        new_selection = new_selection or colorwrap(bg_field, '', cfg)

    with swap_col:
        st.caption("Select colors")
        new_selection = new_selection or buttonswap(fg_field, bg_field, 'Swap tree colors', cfg)

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

    with st.expander("Show advanced options"):
        l = [
            slidewrap('W', 'Full image width', 350, 3500),
            slidewrap('H', 'Full image height', 350, 3500),

            slidewrap('font_size', 'Font size', 12, 44, step = 1, format = '%i pt'),

            dropdownwrap('font_style', 'Text font', cfg['fonts_avail']),

            slidewrap('bottom_padding', 'Padding above nodes (after branched to)', 4, 40, step = 2),
            slidewrap('top_padding', 'Padding below nodes', 4, 40, step = 2),
            colorwrap_cols('fg_color', 'bg_color', cfg),

            slidewrap('margin', 'Margins around the tree', 0, 125)
        ]

    for config in l: # if slidewrap etc has determined a change has been made,
        if config: # i.e. if any of these have returned a truthy value,
            return config # then show_configurations should return that truthy value to tell the app to redraw the tree

    return False


def textbox (old, cfg = st.session_state):
    out = st.text_area(label = "Enter your tree here",
                       value = old,
                       height = len(cfg['sentence'].splitlines()) * 20)

    if out and 'sentence' in cfg and out != cfg['sentence']:
        cfg['sentence'] = out

    if (out != ''):
        return out

    else:
        cfg['sentence'] = '\n'
        return '\n'


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

    if st.session_state['sentence']: # is this useful?
        st.session_state['reload_tree?'] = True

    if show_configurations():
        st.session_state['reload_tree?'] = True

    if new_text != previous_text:
        st.session_state['reload_tree?'] = True
        st.experimental_rerun()
        redraw_tree_if_requested()


    if st.session_state['reload_tree?']:
        redraw_tree_if_requested()


header('pytree', 'Syntax Tree Generator', 'l-acs')
homepage()
