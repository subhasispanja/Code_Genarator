import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 20

if st.button("Click me"):
    st.session_state.count += 1

st.write("Button clicked:", st.session_state.count)
