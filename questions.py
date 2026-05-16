import streamlit as st
import re
import streamlit_sortables as s_t
import random

line = "{type:AudioMatch|question:Match the pairs|options:[ka:audio_match_id1][kha:audio_match_id2][ga:pBHkGEfhEz4B0K5JOg][nga:G5C22UPhE7h3q6KOA7]|id:TW0FMxRNvijh}"

@st.fragment
def render_question(line, question, course):
    debug = st.expander("🪲 Debug")
    with debug:
        st.write(line)
    line = line.split('|')
    if line[0] == '{type:PickOneMeaning':
        st.header("What does this mean?")
        st.write(line[2][7:],":")
        options = line[3][9:-1].split("][")
        one = st.button(options[0], width="stretch", type="primary", key="oneone"+question)
        two = st.button(options[1], width="stretch", type="primary", key="onetwo"+question)
        three = st.button(options[2], width="stretch", type="primary", key="onethree"+question)
        answer = line[-2][7:]
        result = st.container(border=False)
        if one:
            if options[0] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
        elif two:
            if options[1] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
        elif three:
            if options[2] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
    elif 'AudioMatch' in line[0]:
        st.header("Listen and match:")
        options = line[2][9:-1].split("][")
        audios = []
        answers = []
        for line in options:
            line = line.split(':')
            answers.append(line[0])
            audios.append(line[1])
        with debug:
            st.write(audios)
            st.write(answers)
        left, right = st.columns(2)
        with left:
            for item in audios:
                st.audio(f"{course}/{item}.mp3")
        with right:
            correct_answers = answers.copy()
            random.shuffle(answers)
            sorted_items = s_t.sort_items(answers, direction="vertical", key="AudioMatch"+question)
        if st.button("Submit"):
            if sorted_items == correct_answers:
                st.success("Correct!")
            else:
                st.error(f"Nope, it was '{" --> ".join(correct_answers)}'")
    elif 'PickMissingWord' in line[0]:
        st.header(re.sub(r'_[^_]+_', '', line[1][9:]))
        options = line[2][9:-1].split("][")
        one = st.button(options[0], width="stretch", type="primary", key = "twoone"+question)
        two = st.button(options[1], width="stretch", type="primary", key=("twotwo")+question)
        three = st.button(options[2], width="stretch", type="primary", key="twothree"+question)
        four = st.button(options[3], width="stretch", type="primary", key="twofour"+question)
        answer = line[-2][7:]
        result = st.container(border=False)
        if one:
            if options[0] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
        elif two:
            if options[1] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
        elif three:
            if options[2] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
        elif four:
            if options[3] == answer:
                result.success("Correct!")
                return "correct"
            else:
                result.error("No")
                return "incorrect"
    elif 'WriteWords' in line[0]:
        st.header("Translate: '"+line[1][9:]+ "'")
        answer = st.text_area("",key=question)
        submit = st.button("Submit", key="WriteWordsButton"+question)
        if '[' in line[2]:
            answers = line[2][8:1].split("][")
        else:
            answers = []
            answers.append(line[2][7:])
        with debug:
            st.write(answers)
        if submit:
            if answer in answers:
                st.success("Correct")
                return "correct"
            else:
                answer = line[3][15:]
                if answer == '}':
                    answer = line[2][7:]
                st.error(f"No, the correct answer was '{answer}'")
                return "incorrect"
    elif "PickWords" in line[0]:
        words = line[2][9:-1].split("][")
        st.header("Translate: '"+line[1][9:]+ "'")
        items = [
            {"header": "Your answer", "items": []},
            {"header": "Word bank", "items": words}
        ]
        sorted_items = s_t.sort_items(items, multi_containers=True)
        col1, col2, col3 = st.columns([1,2,1])
        if col2.button("Submit", width="stretch", type="primary", key="submit"+question):
            if "".join(sorted_items[0]["items"]) == line[3][7:].replace(",", "").replace("?", "").replace(".", ""):
                st.success("Correct!")
                return "correct"
            else:
                st.error("")
                return "incorrect"
    elif "PickOne" in line[0]:
        st.header(line[1][9:])
        if ")(" in line[2][9:-1]:
            options = line[2][9:-1].split(")(")
        else:
            options = line[2][9:-1].split("][")
        answer = line[3][7:]
        one = st.button(options[0], type="primary", width="stretch", key="threeone"+question)
        two = st.button(options[1], type="primary", width="stretch", key="threetwo"+question)
        three = st.button(options[2], type="primary", width="stretch", key="threethree"+question)
        if one:
            if options[0] == answer:
                st.success("Correct!")
                return "correct"
            else:
                st.error("")
                return "incorrect"
        elif two:
            if options[1] == answer:
                st.success("Correct!")
                return "correct"
            else:
                st.error("")
                return "incorrect"
        elif three:
            if options[2] == answer:
                st.success("Correct!")
                return "correct"
            else:
                st.error("")
                return "incorrect"
    elif "Match" in line[0] and not 'Audio' in line[0]:
        st.header("Sort the items on the right so they match their pair on the left")
        col1, col2 = st.columns(2)
        pairs = line[2][9:-1].split("][")
        with col1:
            index = pairs[0].find(":")
            st.button(pairs[0][:index], type="primary", width="stretch", key="match"+question)
            index = pairs[1].find(":")
            st.button(pairs[1][:index], type="primary", width="stretch", key="match2"+question)
            index = pairs[2].find(":")
            st.button(pairs[2][:index], type="primary", width="stretch", key="match3"+question)
            index = pairs[3].find(":")
            st.button(pairs[3][:index], type="primary", width="stretch", key="match4"+question)
        with col2:

            items = []
            index = pairs[0].find(":")
            items.append(pairs[0][index+1:])
            index = pairs[1].find(":")
            items.append(pairs[1][index+1:])
            index = pairs[2].find(":")
            items.append(pairs[2][index+1:])
            index = pairs[3].find(":")
            items.append(pairs[3][index+1:])
            items_two = items.copy()
            random.shuffle(items)
            sorted_items = s_t.sort_items(items, direction="vertical", key="match_"+question)
        submit_button = st.button("Submit", key="sumbit"+question)
        if submit_button:
            if sorted_items == items_two:
                st.success("Correct!")
                return "correct"
            else:
                st.error("Try again!")
                return "incorrect"
    elif 'FlashCard' in line[0]:
        st.header(f"What is '{line[1][6:]}'?")
        with st.expander("Reveal answer: "):
            st.write(line[2][5:])
    else:
        return "error"

