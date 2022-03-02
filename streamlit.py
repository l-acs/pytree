# https://docs.streamlit.io/library/api-reference
import streamlit as st
from time import sleep
from datetime import datetime
import os

from parse import Parse as p
from convert import Convert
import tree_utils as t


parent_dir = 'out/'
f = parent_dir + t.outfile
sample_f = parent_dir + t.sample_file
h = "pytree — Syntax Tree Generator"

st.set_page_config(
    page_title = h,
)

st.title("pytree")
st.header(h)


if 'config' in st.session_state:
    config = st.session_state['config'].copy()

else:
    config = t.settings.copy() # now we just override this
    st.session_state['config'] = config.copy()

if 'sentence' not in st.session_state:
    st.session_state['sentence'] = t.sample

tree_text = st.session_state['sentence']




fonts = [font_file.split('.')[0] for font_file in os.listdir('fonts/')]
fonts.sort()

def default_tree (filename = sample_f):
    tree = t.create_tree(t.sample)
    image = t.save_tree(tree, filename)
    return filename

def gen_default_tree_if_not_exists (fname = sample_f):
    if not(os.path.exists(fname)):
        default_tree(fname)
    

def st_show_tree (fname = sample_f):
    # make sure we at least have the default
    if fname == sample_f:
        gen_default_tree_if_not_exists(fname)

    if os.path.exists(fname):
        with open(fname, "rb") as file:
            st.image(fname)
    else:
        st.warning("Error showing tree image!")


def filename_for_download (filename_prefix = 'tree', filetype = 'png'):
    date_exp = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()

    return filename_prefix + now.strftime(date_exp) + '.' + filetype


def btn_download_tree(fname = f):
    with open(fname, "rb") as file:
        if file:
            btn = st.download_button(
                label="Download tree",
                data=file,
                file_name= filename_for_download(),
                mime="image/png"
            )
            return btn


tree_gen_form = st.form("tree_gen")

tree_text = tree_gen_form.text_area(label = "Enter your tree here:",
                                    value = st.session_state['sentence'],
                                    height = len(st.session_state['sentence'].splitlines()) * 20)


# put advanced features here
with st.expander("Show advanced features"):
    config["font_style"] = tree_gen_form.selectbox('Select a font:', fonts)

    config["font_size"] = int(4 * tree_gen_form.number_input('Choose font size:', min_value=8, max_value=40, value = 20))
    config["fg_color"] = tree_gen_form.color_picker('Pick line and text color:', "#42A6D0") # use something other than the actual default to be more illustrative; otherwise it (seems like it) stays black as you move the slider)

    config["thickness"] = tree_gen_form.slider('Thickness of lines:', 0, 15, t.settings["thickness"])

    config["top_padding"] = tree_gen_form.slider("Padding between parent node and the line(s) below it:",
                                      0, 40, value = t.settings["top_padding"])

    config["bottom_padding"] = tree_gen_form.slider("Padding between a line and the node underneath:",
                                      0, 40, value = t.settings["bottom_padding"])

    config["W"] = tree_gen_form.slider('Full image width in pixels:', 350, 3500, t.settings["W"] )
    config["H"] = tree_gen_form.slider('Full image height in pixels:', 350, 3500, t.settings["H"])
    config["margin"] = tree_gen_form.slider('Approximate margins around the tree:', 0, 100, t.settings["margin"])


run = tree_gen_form.form_submit_button("Generate this tree")

if run:
    st.session_state['config'] = config
    st.session_state['sentence'] = tree_text

    try:
        with st.spinner(text="Generating your tree..."):
            parsed_tree = Convert(string = tree_text).to_tree()
            image = t.save_tree(parsed_tree, f, cfg = config)

            st_show_tree(f)
            st.success("Your tree has been generated!")


    except p.ParseError:
        st.warning("It looks like that's not a valid tree! Please edit your text and try again.")




# now run this as:
# streamlit run this_file_path
# (from root of repository, as that's where paths are relative to)
