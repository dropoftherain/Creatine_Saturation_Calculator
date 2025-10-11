import streamlit as st

st.title('blabla')

if "weight_key" not in st.session_state:
    st.session_state.weight_key = 70

weight = st.slider('Weight in kg', 45, 100, key="weight_key")
height = st.slider('Height in cm', 145, 215, key="height_key")


st.write(st.session_state.weight_key)