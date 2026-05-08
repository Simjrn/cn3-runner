import streamlit as st
import questions as q
from streamlit_extras.card_selector import *
import re
import pandas as pd


def translate_to_standard_md(text):
    #<image:img_LMJskZwdHsKZ_1764187126150.png/>
    if not text.startswith("<image:"):
        text = re.sub(r'\^\^(.+?)\^\^', r'# \1', text)
        text = re.sub(r'(?<!\^)\^([^\^]+?)\^(?!\^)', r'## \1', text)
        text = re.sub(r'\*(?!\s)(.+?)(?<!\s)\*', r'**\1**', text)
        text = re.sub(r'_([^_]+?)_', r'*\1*', text)
        return text




def split_list_by_string(original_list, trigger_string):
    sections = []
    current_section = []

    for item in original_list:
        # Check if the current line starts with your specific string
        if item.startswith(trigger_string):
            # If the current_section isn't empty, save it before starting a new one
            if current_section:
                sections.append(current_section)
            current_section = [item] # Start the new section with the trigger line
        else:
            current_section.append(item)

    # Don't forget to add the last section after the loop finishes
    if current_section:
        sections.append(current_section)
        
    return sections



@st.fragment
def create_path(unit, course):
    # Initialize state to track what to show
    if "current_view" not in st.session_state:
        st.session_state.current_view = "main"

    placeholder = st.empty()

    with placeholder.container():
        # --- VIEW 1: Main Path ---
        if st.session_state.current_view == "main":
            with open(f"{course}/unit{unit}.nml", "r") as f:
                for line in f:
                    if line.startswith("<unit:"):
                        st.header(line[1:-2].replace(":", " "))
                    
                    elif line.startswith("<skill:"):
                        line_parts = line.split("|")
                        skill_name = line_parts[0][7:]
                        # Use a callback to update state safely
                        if st.button(skill_name, key=f"btn_{skill_name}", width="stretch"):
                            st.session_state.current_view = skill_name
                            st.rerun() # Refresh to show the new view
        elif st.session_state.current_view == "questions":
            counter = st.session_state.counter
            lessons = st.session_state.lessons
            num = st.session_state.num
            if not num >= len(lessons[counter-1]):
                error = q.render_question(lessons[counter-1][num], str(num))
                num += 1
                st.session_state.num = num
                if error:
                    st.rerun()
                if st.button("Next", width="stretch"):
                    st.rerun()
            else:
                st.title("Lesson completed!")
                st.balloons()
                if st.button("Next", width="stretch"):
                    st.session_state.current_view = "main"
                    st.rerun()


        # --- VIEW 2: Skill Detail ---
        else:
            skill_name = st.session_state.current_view
            st.write(f"### {skill_name}")
            with open(f"{course}/unit{unit}.nml", "r") as f:
                for line in f:
                    if line.startswith("<skill:"+skill_name):
                        st.write("**"+line.split("|")[6][12:]+"**")
                        start_marker = line
                        end_marker = "</skill>" # Looking for the next unit tag regardless of number
                        inside = False
                        results = []
                        with open(f"{course}/unit{unit}.nml", "r") as f:
                            for line in f:
                                if line.startswith(start_marker):
                                    inside = True
                                    continue 
                                if inside:
                                    if line.startswith(end_marker):
                                        break
                                    results.append(line.strip())
                        lessons = split_list_by_string(results, '<lesson:')
                counter = 0
                for item in results:
                    if item.startswith("<lesson:"):
                        counter += 1
                        if st.button(item.split("|")[0][1:].replace(":", " ")):
                            st.session_state.current_view = "questions"
                            st.session_state["counter"] = counter
                            st.session_state["lessons"] = lessons
                            st.session_state.num = 1
                            st.rerun()
            page = card_selector(
                [
                    dict(icon="📚", title="Notes", description="See the notes for this skill"),
                    dict(icon="🗨", title="Sentences", description="See the sentences you will be tested on in this skill"),
                    dict(icon="🔤", title="Words", description="See the words and phrases introduced in this section")
                ]
            )
            if page == 0:
                with open(f"{course}/unit{unit}.nml") as f:
                    for line in f:
                        if line.startswith("<skill:"+skill_name):
                            line = line.split("|")
                            id = line[-1][3:-2]
                            with open(f"{course}/{id}.ntf") as notes:
                                for line in notes:
                                    md = translate_to_standard_md(line)
                                    if md:
                                        st.markdown(md)
                                    else:
                                        st.image(f"{course}/"+line[7:-3].replace("*", "_"))
            if page == 1:
                with open(f"{course}/unit{unit}.nml") as f:
                    for line in f:
                        if line.startswith("<skill:"+skill_name):
                            line = line.split("|")
                            id = line[-1][3:-2]
                            with open(f"{course}/{id}.sentences") as sentences:
                                base = {}
                                for line in sentences:
                                    if not counter == 0:
                                        line = line.split("|")
                                        base[line[0]] = line[1]
                                # Creates a table with 2 columns: "ID" and "Sentence"
                                df = pd.DataFrame(base.items(), columns=['Romansh', 'English'])
                                df = df[1:]
                                st.dataframe(df)
            elif page == 2:
                with open(f"{course}/unit{unit}.nml") as f:
                    for line in f:
                        if line.startswith("<skill:"+skill_name):
                            line = line.split("|")
                            id = line[-1][3:-2]
                            with open(f"{course}/{id}.vocab") as vocab:
                                base = {}
                                for line in vocab:
                                    line = line[2:-3].split("}{")
                                    base[line[0]] = line[1]
                                df = pd.DataFrame(base.items(), columns=['Term', 'Translation'])
                                df = df[1:]
                                st.dataframe(df)
            if st.button("Back to Path", type="primary"):
                st.session_state.current_view = "main"
                st.rerun()

