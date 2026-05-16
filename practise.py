from streamlit_extras.floating_button import *

@st.fragment
def practise_page(unit, course) -> None:
    mode = st.segmented_control("How would you like to practise?", ["Flashcards", "Practise lesson"])
    if mode == "Flashcards":
        with open(f"{course}/unit{unit}.nml") as f:
            skills = []
            for line in f:
                if line.startswith("<skill:"):
                    line = line.split("|")
                    skill_name = line[0][7:]
                    skills.append(skill_name)
            chosen_skill = st.selectbox("Choose which skill you would like to practise",skills)
            submit = st.button("Start:")
            if submit:
                with open(f"{course}/unit{unit}.nml") as unit:
                    for line in unit:
                        if line.startswith(f"<skill:{chosen_skill}"):
                            line = line.split("|")
                            id = line[-1][3:-2]
                            words = []
                            with open(f"{course}/{id}.vocab") as f:
                                for line in f:
                                    words.append(line[2:-3].split('}{'))
def flashcards(items, counter)
    st.header(item[0])
    with st.expander("Show answer:"):
        st.write(item[1])



if floating_button("🏋 Practise"):
    practise_page(0, 'Romansh(standard)')