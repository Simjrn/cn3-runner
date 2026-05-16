import streamlit as st
from interface import create_path
from streamlit_image_select import image_select



num = st.sidebar.selectbox("What unit are you studying?", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
switch = st.sidebar.expander("Switch language")
def switch_lang():
    opt = image_select(
        label="Select your language: ",
        images=[
            "Dutch.png",
            "Finnish.png",
            "Burmese.png",
            "Romansh(standard).png"
        ],
        captions= ["Dutch", "Finnish", "Burmese", "Rumantsch grischun"]
    )
    return opt

with switch:
    lang = switch_lang()
    lang = lang[:-4]

create_path(num, lang)