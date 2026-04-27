import streamlit as st
import re
import streamlit_sortables as s_t

line = "{type:PickWords|question:El è bain|options:[is][He][She][well]|answer:Heiswell|answerviewable:He is well|id:Xr6TDICdglEB}"
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
                result.success("Correct!")
            else:
                result.error("No")
        elif two:
            if options[1] == answer:
                result.success("Correct!")
            else:
                result.error("No")
        elif three:
            if options[2] == answer:
                result.success("Correct!")
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
                result.success("Correct!")
            else:
                result.error("No")
        elif two:
            if options[1] == answer:
                result.success("Correct!")
            else:
                result.error("No")
        elif three:
            if options[2] == answer:
                result.success("Correct!")
            else:
                result.error("No")
        elif four:
            if options[3] == answer:
                result.success("Correct!")
            else:
                result.error("No")
    elif 'WriteWords' in line[0]:
        st.header("Translate: '"+line[1][9:]+ "'")
        answer = st.text_area("")
        submit = st.button("Submit")
        if submit:
            if answer == line[2][7:]:
                st.success("Correct")
            else:
                st.error("")
    elif "PickWords" in line[0]:
        words = line[2][9:-1].split("][")
        st.header("Translate: '"+line[1][9:]+ "'")
        items = [
            {"header": "Your answer", "items": []},
            {"header": "Word bank", "items": words}
        ]
        sorted_items = s_t.sort_items(items, multi_containers=True)
        col1, col2, col3 = st.columns([1,2,1])
        if col2.button("Submit", width="stretch", type="primary"):
            if "".join(sorted_items[0]["items"]) == line[3][7:]:
                st.success("Correct!")
            else:
                st.error("")
        





render_question(line)


