import streamlit as st
import questions as q

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
def create_path():
    # Initialize state to track what to show
    if "current_view" not in st.session_state:
        st.session_state.current_view = "main"

    placeholder = st.empty()

    with placeholder.container():
        # --- VIEW 1: Main Path ---
        if st.session_state.current_view == "main":
            with open("course/unit0.nml", "r") as f:
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
                q.render_question(lessons[counter-1][num], str(num))
                num += 1
                st.session_state.num = num
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
            with open("course/unit0.nml", "r") as f:
                for line in f:
                    if line.startswith("<skill:"+skill_name):
                        st.write("**"+line.split("|")[6][12:]+"**")
                        start_marker = line
                        end_marker = "</skill>" # Looking for the next unit tag regardless of number
                        inside = False
                        results = []
                        with open("course/unit0.nml", "r") as f:
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
                            st.session_state.num = 0
                            st.rerun()
            if st.button("Back to Path", type="primary"):
                st.session_state.current_view = "main"
                st.rerun()

create_path()
