# https://docs.streamlit.io/library/api-reference
import streamlit as st
from time import sleep
from datetime import datetime
from os.path import exists

# temporarily:
import sys
sys.path.append("/home/l-acs/projects/python/pytree")

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



def default_tree (filename = parent_dir + t.outfile):
    tree = t.create_tree(t.sample)
    image = t.save_tree(tree, filename)
    # image.show()
    # t.save_tree(tree, filename)
    return filename

def gen_tree_if_not_exists (fname = parent_dir + t.outfile):
    if not(exists(fname)):
        default_tree(fname)
    

def st_show_tree (fname = parent_dir + t.outfile):
    gen_tree_if_not_exists(fname)

    if exists(fname):
        with open(fname, "rb") as file:
            st.image(f)
    else:
        st.warning("Error showing tree image!")
        
def filename_for_download (filename_prefix = 'tree', filetype = 'png'):
    date_exp = "%Y-%m-%d_%H:%M:%S"
    now = datetime.now()

    return filename_prefix + now.strftime(date_exp) + '.' + filetype



# now run streamlit s.t. you see the image!

st_show_tree(f)
# tree_text = st.text_input(label = "Enter your tree here:",


# https://docs.streamlit.io/library/api-reference/widgets/st.text_area
tree_text = st.text_area(label = "Enter your tree here:",
                         value = t.sample,
                         height = len(t.sample.splitlines()) * 20)



# NOTE: this does *not* yet parse new trees. It's just the example for now


progress_bar = st.checkbox("Show progress bar")

with open(f, "rb") as file:
    if file:
        btn = st.download_button(
            label="Download tree",
            data=file,
            file_name= filename_for_download(),
            mime="image/png"
        )

if progress_bar:
    latest_iteration = st.empty()
    bar = st.progress(0)
    sleep_time = 0.05

    for i in range(100):
        latest_iteration.text(f'{i+1}% complete...')
        bar.progress(i + 1)

        if (i == 10):
            sleep_time = 0.01

        # if (i == 70):
        #     sleep_time = 0.02

        if (i == 90):
            sleep_time = 0.05

        if (i == 95):
            sleep_time = 0.1

        # print(sleep_time)
        sleep(sleep_time)
        if (i > 40 and i < 80):
            i += 1



        
    st.balloons()
    st.success("Your tree has been generated!")

# now run me as
# streamlit run this_file_path
# (from root of repository, as that's where paths are relative to)

            
