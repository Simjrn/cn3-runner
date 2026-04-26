import streamlit as st
import re

line = "{type:PickMissingWord|question:Allegra, co ___vai___?|options:[Bain][Allegra][Co vai?][vai]|answer:vai|id:AoYKyORCZiOU}"
@st.fragment
def render_question(line):
    line = line.split('|')
    if 'PickOneMeaning' in line[0]:
        st.header("What does this mean?")
        st.write(line[2][7:],":")
        options = line[3][9:-1].split("][")
        one = st.button(options[0], width="stretch", type="primary")
        two = st.button(options[1], width="stretch", type="primary")
        three = st.button(options[2], width="stretch", type="primary")
        answer = line[-2][7:]
        result = st.container(border=False)
        if one:
            if options[0] == answer:
                result.info("Correct!")
            else:
                result.error("No")
        elif two:
            if options[1] == answer:
                result.info("Correct!")
            else:
                result.error("No")
        elif three:
            if options[2] == answer:
                result.info("Correct!")
            else:
                result.error("No")
    elif 'PickMissingWord' in line[0]:
        st.header(re.sub(r'_[^_]+_', '', line[1][9:]))
        options = line[2][9:-1].split("][")
        one = st.button(options[0], width="stretch", type="primary")
        two = st.button(options[1], width="stretch", type="primary")
        three = st.button(options[2], width="stretch", type="primary")
        four = st.button(options[3], width="stretch", type="primary")
        answer = line[-2][7:]
        result = st.container(border=False)
        if one:
            if options[0] == answer:
                result.info("Correct!")
            else:
                result.error("No")
        elif two:
            if options[1] == answer:
                result.info("Correct!")
            else:
                result.error("No")
        elif three:
            if options[2] == answer:
                result.info("Correct!")
            else:
                result.error("No")
        elif four:
            if options[3] == answer:
                result.info("Correct!")
            else:
                result.error("No")



render_question(line)


