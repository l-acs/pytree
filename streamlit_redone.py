import streamlit as st
import tree_utils as t
from parse import Parse as p

def set_defaults_if_empty (cfg = st.session_state, defaults = t.settings):
    for k in defaults:
        if k not in cfg:
            cfg[k] = defaults[k]
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
        st.write('requested')

        if reparse: # this probably shouldn't go here?
            parse(cfg)

        gen_tree_image(cfg, f = cfg['default_file'] if default else cfg['output_file'])
        set_tree_container_if_not_exists()
        reload_tree(cfg, default)
        st.session_state['reload_tree?'] = False
    else:
        st.write('not requested')



def slidewrap(cfield, label, minv, maxv, step = 5, format = '%i pixels', cfg = st.session_state):
    cfg[cfield] = st.slider(label = label,
                    value = cfg[cfield],
                    min_value = minv,
                    max_value = maxv,
                    step = step,
                    format = format
    )


def show_configurations (cfg = st.session_state):
    with st.expander("Show advanced options"):
        slidewrap('W', 'Width of the whole image', 350, 3500)
        slidewrap('H', 'Height of the whole image', 350, 3500)
        slidewrap('top_padding', 'Top padding between node and branches', 4, 40, step = 2)
        slidewrap('bottom_padding', 'Bottom padding between branches and nodes', 4, 40, step = 2)

def header ():
    
    st.write('sth')




def homepage ():
    set_defaults_if_empty()
    initial_draw()

    # with st.expander("Show current state"):
    #     state_keys = [k for k in st.session_state]
    #     state_keys.sort()
    #     for k in state_keys:
    #         st.write(f"{k} has value {st.session_state[k]} in st.session_state")


    generate_tree = st.button("Generate this tree!")
    # st.write(generate_tree)
    st.session_state['reload_tree?'] = generate_tree
    # st.write(generate_tree)
    # st.write(st.session_state['reload_tree?'])
    # st.checkbox("this has no real function except to test page reloads :)")

    ####
    # this is the big if
    # if it doesn't do as intended, forget it for now
    s = st.text_area(label = "this may do a thing?",
                     value = st.session_state['sentence'])

    if s != '':
        st.session_state['sentence'] = s
        #### 
        
        # ###                                                        ###
        # try: also reload the tree whenever this changes!             #
                                                                       
        # st.session_state['reload_tree?'] = True                      #
        # it doesn't quite do the trick:(                              #
        # it made changes happen dynamically - which was cool - but it #
        # only occured on every second change, which was weird         #
        # ###                                                        ###



    show_configurations()

    # okay, I think this is a logical improvement!
    ####
    redraw_tree_if_requested(reparse = True)

header()
homepage()
