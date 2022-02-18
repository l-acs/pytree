# https://docs.streamlit.io/library/api-reference
import streamlit as st
from time import sleep
from datetime import datetime
from os.path import exists

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

tree_graphic = st.empty() # placeholder that will be filled with the auto-updating tree


def default_tree (filename = sample_f):
    tree = t.create_tree(t.sample)
    image = t.save_tree(tree, filename)
    return filename

def gen_default_tree_if_not_exists (fname = sample_f):
    if not(exists(fname)):
        default_tree(fname)
    

def st_show_tree (fname = sample_f, tree_container = tree_graphic):
    # # hide the tree for now
    # tree_container.empty()

    # make sure we at least have the default
    if fname == sample_f:
        gen_default_tree_if_not_exists(fname)

    if exists(fname):
        with open(fname, "rb") as file:
            with tree_container.container():
                st.image(fname)
    else:
        st.warning("Error showing tree image!")


def filename_for_download (filename_prefix = 'tree', filetype = 'png'):
    date_exp = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()

    return filename_prefix + now.strftime(date_exp) + '.' + filetype


# now run streamlit s.t. you see the image!
st_show_tree() # shows default image

# https://docs.streamlit.io/library/api-reference/widgets/st.text_area
tree_text = st.text_area(label = "Enter your tree here:",
                         value = t.sample,
                         height = len(t.sample.splitlines()) * 20)

progress_bar = st.checkbox("Show progress bar", value = True)
left_button, right_button, _ = st.columns([1, 1, 2]) # (2)

def btn_generate_tree(button_column = left_button, key = "default"):
    with button_column:
        result = st.button("Generate this tree", key=key)

    return result


def btn_download_tree(button_column = right_button, fname = f):
    with open(fname, "rb") as file:
        if file:
            with button_column:
                btn = st.download_button(
                    label="Download tree",
                    data=file,
                    file_name= filename_for_download(),
                    mime="image/png"
                )
                return btn

# show the plain generate button
generate_tree = btn_generate_tree(left_button)


if generate_tree and tree_text:
    # hide the tree for now
    tree_graphic.empty()

    try:
        with tree_graphic.empty():
            if progress_bar: # stalling
                parsed_tree = Convert(string = tree_text).to_tree()
                image = t.save_tree(parsed_tree, f)

                latest_iteration = st.empty()
                bar = st.progress(0)
                sleep_time = 0.05

                for i in range(100):
                    latest_iteration.text(f'{i+1}% complete...')
                    bar.progress(i + 1)

                    if (i == 10):
                        sleep_time = 0.01

                    if (i == 90):
                        sleep_time = 0.05

                    if (i == 95):
                        sleep_time = 0.1

                    sleep(sleep_time)
                    if (i > 40 and i < 80):
                        i += 1

            else:
                with st.spinner(text="Generating your tree..."):
                    parsed_tree = Convert(string = tree_text).to_tree()
                    image = t.save_tree(parsed_tree, f)

                # st.balloons() # maybeeee


                # update the onscreen graphic
        st_show_tree(f)
        st.success("Your tree has been generated!")

        # provide download button
        btn_download_tree(right_button, f)


    except p.ParseError:
        st.warning("It looks like that's not a valid tree! Please edit your text and try again.")
        tree_graphic.empty()


# now run this as:
# streamlit run this_file_path
# (from root of repository, as that's where paths are relative to)
