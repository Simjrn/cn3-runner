import streamlit as st
from interface import create_path

num = st.selectbox("What unit are you studying?", (0, 1, 2, 3, 4))

create_path(num, "Rumantsh-grischun")