import streamlit as st
import tree_utils as t
from parse import Parse as p
import os

def set_defaults_if_empty (cfg = st.session_state, defaults = t.settings):
    for k in defaults:
        if k not in cfg:
            cfg[k] = defaults[k]


def set_fonts_if_empty (cfg = st.session_state, loc = 'fonts/'):
    if 'fonts_avail' not in cfg:
        fonts = [font_file.split('.')[0] for font_file in os.listdir('fonts/')]
        fonts.sort()
        cfg['fonts_avail'] = fonts


def set_tree_container_if_not_exists (cfg = st.session_state):
    if 'tree_container' not in cfg:
        cfg['tree_container'] = st.empty()


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

def redraw_tree_if_requested (cfg = st.session_state, default = False):
    if 'reload_tree?' in cfg and cfg['reload_tree?']:

        if 'sentence' in cfg and cfg['sentence']:
            p = parse(cfg)
            if not (p): # failed parse
                return # exit

        gen_tree_image(cfg, f = cfg['default_file'] if default else cfg['output_file'])
        set_tree_container_if_not_exists()
        reload_tree(cfg, default)
        cfg['reload_tree?'] = False


def inform_of_reload (field, widget_field, cfg = st.session_state, check = lambda x: True, fallback = True): # callback for widget changes
    cfg['reload_tree?'] = True
    cfg[field] = cfg[widget_field] if check(cfg[widget_field]) else fallback

def swap_and_inform_of_reload (cfield1, cfield2, cfg = st.session_state):
    tmp = cfg[cfield1]
    cfg[cfield1] = cfg[cfield2]
    cfg[cfield2] = tmp
    cfg['reload_tree?'] = True

def slidewrap(cfield, label, minv, maxv, step = 5, format = '%i pixels', cfg = st.session_state):
    slider_name = cfield + '_slider'
    st.slider(label = label,
              value = cfg[cfield], # previous value
              min_value = minv,
              max_value = maxv,
              step = step,
              format = format,
              key = slider_name, # this will make it accessible in state
              on_change = inform_of_reload,
              args = (cfield, slider_name, cfg))


def colorwrap(cfield, label, cfg = st.session_state):
    picker_name = cfield + '_picker'
    st.color_picker(label = label,
                    value = cfg[cfield], # previous value
                    key = picker_name, # this will make it accessible in state
                    on_change = inform_of_reload,
                    args = (cfield, picker_name, cfg))


def buttonswap(cfield1, cfield2, label, cfg = st.session_state):
    button_name = f'{cfield1}_{cfield2}_buttonswap' # unique id for this swap button

    st.button(label = label,
              key = button_name,
              on_click = swap_and_inform_of_reload,
              args = (cfield1, cfield2, cfg))


def colorwrap_cols (fg_field = 'fg_color', bg_field = 'bg_color', cfg = st.session_state):
    swap_col, fg_col, bg_col = st.columns([10, 1, 4])

    with fg_col:
        colorwrap(fg_field, '', cfg)

    with bg_col:
        colorwrap(bg_field, '', cfg)

    with swap_col:
        st.caption("Select colors")
        buttonswap(fg_field, bg_field, 'Swap tree colors', cfg)


def dropdownwrap(cfield, label, options, cfg = st.session_state):
    # seems like this occasionally returns some garbage and doesn't
    # reload the tree?? but only rarely. Can't figure out how to
    # consistently reproduce. Hmm

    prev = cfg[cfield]
    options_tweaked = t.reorder_insert_at_top(options, prev) # fixes [unwanted [font reset]] on update

    out = st.selectbox(label, options_tweaked)

    if out and out != prev:
        cfg[cfield] = out
        cfg['reload_tree?'] = True
        st.experimental_rerun() # this is the key bit
        return True

    else:
        return False


def show_configurations (cfg = st.session_state):
    with st.expander("Show advanced options"): # possible bug: first change closes the expander
        slidewrap('W', 'Full image width', 350, 3500)
        slidewrap('H', 'Full image height', 350, 3500)

        slidewrap('font_size', 'Font size', 12, 44, step = 1, format = '%i pt')
        dropdownwrap('font_style', 'Text font', cfg['fonts_avail'])

        slidewrap('bottom_padding', 'Padding above nodes (after branched to)', 4, 40, step = 2)
        slidewrap('top_padding', 'Padding below nodes', 4, 40, step = 2)

        colorwrap_cols('fg_color', 'bg_color', cfg)
        slidewrap('margin', 'Margins around the tree', 0, 125)


def textbox (cfield, cfg = st.session_state):
    area_name = cfield + '_textbox'
    old = cfg[cfield]
    st.text_area(label = "Enter your tree here",
                 value = old,
                 height = len(old.splitlines()) * 20,
                 key = area_name,
                 on_change = inform_of_reload,
                 args = (cfield, area_name, cfg),
                 kwargs = {'check': t.sanity_check, 'fallback': '\n'})


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


def homepage (cfg = st.session_state):
    set_defaults_if_empty()
    set_fonts_if_empty()

    textbox('sentence', cfg)
    show_configurations()
    redraw_tree_if_requested()


header('pytree', 'Syntax Tree Generator', 'l-acs')
homepage()
