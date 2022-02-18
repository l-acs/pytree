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
h = "pytree — Syntax Tree Generator"

st.set_page_config(
    page_title = h,
)

st.title("pytree")
st.header(h)

tree_graphic = st.empty() # placeholder that will be filled with the auto-updating tree


def default_tree (filename = parent_dir + t.outfile):
    tree = t.create_tree(t.sample)
    image = t.save_tree(tree, filename)
    # image.show()
    # t.save_tree(tree, filename)
    return filename

def gen_tree_if_not_exists (fname = parent_dir + t.outfile):
    if not(exists(fname)):
        default_tree(fname)
    

def st_show_tree (fname = parent_dir + t.outfile, tree_container = tree_graphic):
    gen_tree_if_not_exists(fname)

    if exists(fname):
        with open(fname, "rb") as file:
            with tree_container.container():
                st.image(f)

    else:
        st.warning("Error showing tree image!")
        
def filename_for_download (filename_prefix = 'tree', filetype = 'png'):
    date_exp = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()

    return filename_prefix + now.strftime(date_exp) + '.' + filetype


# now run streamlit s.t. you see the image!
st_show_tree(f)

# https://docs.streamlit.io/library/api-reference/widgets/st.text_area
tree_text = st.text_area(label = "Enter your tree here:",
                         value = t.sample,
                         height = len(t.sample.splitlines()) * 20)

progress_bar = st.checkbox("Show progress bar")

generate_tree = st.button("Generate this tree")

if generate_tree and tree_text:
    try:

        parsed_tree = Convert(string = tree_text).to_tree()
        image = t.save_tree(parsed_tree, f)

        if progress_bar: # stalling
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

            # st.balloons() # maybeeee


        # update the onscreen graphic
        st_show_tree(f)
        st.success("Your tree has been generated!")

        # provide download button
        with open(f, "rb") as file:
            if file:
                btn = st.download_button(
                    label="Download tree",
                    data=file,
                    file_name= filename_for_download(),
                    mime="image/png"
                ) # todo: use a container so that it's side by side with the generate button

    except p.ParseError:
        st.warning("It looks like that's not a valid tree! Please edit your text and try again.")


# now run this as:
# streamlit run this_file_path
# (from root of repository, as that's where paths are relative to)

# todo: handle invalid input gracefully


# todo: always start with the same image, default.png
# (doesn't yet exist)

# which should match t.sample
