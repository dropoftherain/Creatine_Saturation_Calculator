# Application interface

import streamlit as st
from scipy.integrate import odeint
import pandas as pd
from calculation import test_import
from calculation import simulate_creatine
import constants as c

st.title('Creatine Saturation Calculator')

# if "weight_key" not in st.session_state:
    # st.session_state.weight_key = 70

# INPUTS
weight = st.slider('Weight in kg', min_value=45, max_value=100, value=70, key="weight_key")
# HEIGHT = st.slider('Height in cm', min_value=145, max_value=215, value=180, key="height_key")
sex = st.segmented_control("Sex", ["Female", "Male"], selection_mode="single", key="sex_key")
activity_strings = ["Not very active", "Active", "Athlete/Body builder"]
selected_act_level = st.select_slider("Activity level", options=activity_strings, key="activity_key")
activity_level = activity_strings.index(selected_act_level) + 1
time_of_simulation = st.number_input('How many days should the simulation be?', 
                                             min_value=1, max_value=30, value=10, key="simulation_days_key")
time_between_doses = st.number_input('Time between doses in hours', min_value=6, max_value=24, key="time_doses_key")        
loading_phase = st.number_input("How many days of loading phase?", min_value=1, max_value=15, key="loading_key")
loading_dose = 1000*(st.number_input("Loading dose of creatine in grams", min_value=5, max_value=25, key="loading_dose_key"))
keeping_dose = 1000*(st.number_input("Keeping dose of creatine in grams", min_value=5, max_value=10, key="keeping_dose_key")) 

# st.write(st.session_state.weight_key)
st.write("Total hours of simulation", test_import(time_of_simulation, time_between_doses))

# Trying if the simulation runs
conc_t, conc_s, m_all_muscles_kg, C_M_end = simulate_creatine(weight, sex, activity_level, time_of_simulation, time_between_doses, loading_phase, loading_dose, keeping_dose)
st.write("Dry muscles in kg", round(m_all_muscles_kg, 2))
st.write("Ending creatine muscle concentration in mmol/kg", round(C_M_end, 2))