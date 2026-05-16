import streamlit as st
from streamlit_extras.floating_button import *
data = '<metadata|visiblename:Sursilvan Romansh|language:ukrainian|attribution:Simjrn|units:1|flag:switzerland|version:0.0.2>'
def metadata(line):
    if floating_button("ℹ Information"):
        @st.dialog("Metadata")
        def show_data(line):
            line = line.split("|")
            st.write(line[1][7:].replace(":", ": **")+'**')
            st.write(line[2].replace(":", ": **")+'**')
            st.write(line[3].replace(":", ": **")+'**')
            st.write(line[4].replace(":", ": **")+'**')
            st.write(line[6][:-1].replace(":", ": **")+'**')
        show_data(line)
