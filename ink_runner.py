import streamlit as st
ink = """title:How are you?

bold:Tom is walking in the park
bold:He sees his friend, Jack

Jack: Bun di, Tom
Tom: Allegra, co vai?
Jack: Bain, grazia e ti?
Tom: Bain, ma fitg stanchel

bold:How is Tom feeling?
+ Tired -> Tired
+ Annoyed -> Wrong

=== Tired ===
bold:Well done!

=== Wrong ===
bold:Nope, the correct answer was 'Tired'
"""
@st.fragment
def process_ink(ink, rerun):
    if rerun == "False":
        ink = ink.splitlines()
    key = 0
    for item in ink:
        if item.startswith("title:"):
            st.title(item[6:])
        elif item.startswith("bold:"):
            st.write(f"**{item[5:]}**")
        elif item.startswith("+"):
            counter = 0
            parts = {}
            for line in ink:
                if line.startswith("==="):
                    name = line[4:-4]
                    parts[name] =[]
                    for line in ink[counter+1:]:
                        if not line.startswith("==="):
                            parts[name].append(line)
                        else:
                            break
                counter += 1
            end_index = item.find("->")
            label = item[1:end_index]
            con = st.container()
            with con:
                col1, col2, col3 = st.columns([1,1,1], vertical_alignment="center")
                button = col3.button(label, type="tertiary", key=key)
            if button:
                index = end_index + 3
                label = item[index:]
                result = label
                process_ink(parts[result], rerun="True")
        elif item.startswith("==="):
            break
        else:
            st.write(item)
        key += 1
process_ink(ink, rerun="False")