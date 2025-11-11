# Calculation and simulation

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
import plotly.graph_objects as go
import pandas as pd
import constants as c

def test_import(TIME_OF_SIMULATION_IN_DAYS, TIME_BETWEEN_DOSING):
    TIME_END = 24 * TIME_OF_SIMULATION_IN_DAYS / TIME_BETWEEN_DOSING
    return TIME_END

def simulate_creatine(WEIGHT, SEX, ACTIVITY_LEVEL, TIME_OF_SIMULATION_IN_DAYS, TIME_BETWEEN_DOSING, LOADING_PHASE, LOADING_DOSE, KEEPING_DOSE):
    
    TIME_END = 24 * TIME_OF_SIMULATION_IN_DAYS / TIME_BETWEEN_DOSING        # Number of intervals 
    KEEPING_SATURATION_PHASE = TIME_OF_SIMULATION_IN_DAYS - LOADING_PHASE   # Days of simulation with keeping dose
    LOADING_END = int(24 * LOADING_PHASE / TIME_BETWEEN_DOSING)             # Number intervals with loading dose

    def calculate_muscle_fraction(ACTIVITY_LEVEL, SEX):
        if SEX == "Female":
            MUSCLE_FRACTION = 0.28 + ACTIVITY_LEVEL * 0.035
        if SEX == "Male":
            MUSCLE_FRACTION = 0.31 + ACTIVITY_LEVEL * 0.05
        return MUSCLE_FRACTION

    MUSCLE_FRACTION = calculate_muscle_fraction(ACTIVITY_LEVEL, SEX)        # Personalized dry muscle fraction parameter of the body
    M_ALL_MUSCLES_KG = c.DRY_FRACTION * MUSCLE_FRACTION * WEIGHT            # Personalized dry muscle fraction [kg]
    CR_MAX = c.CR_MAX_PER_KG * c.MW_CR * M_ALL_MUSCLES_KG                   # Maximum creatine muscle capacity [mg dry] 

    def calculate_initial_creatine_level(m_muscles):
        n = c.C_M_0 * M_ALL_MUSCLES_KG                                      # Personalized amount of moles of baseline creatine [mmol] 
        x_m_0 = n * c.MW_CR                                                 # Personalized amount of baseline creatine [mg]
        return x_m_0

    # Simulation Initial Conditions
    X_A_0 = 1000                                                            # Creatine amount initially in gut [mg]
    X_P_0 = 2000                                                            # Creatine amount initially in plasma [mg]
    X_M_0 = calculate_initial_creatine_level(M_ALL_MUSCLES_KG)              # Personalized creatine amount initially in the muscles [mg]
    S_0 = [X_A_0, X_P_0, X_M_0]

    def creatine_model(S,t):
        X_A, X_P, X_M = S
        C_P = X_P / c.V_D                                                   # Plasma concentration [mg/L]
        absorption = c.V_MAX * X_A / (c.K_M + X_A)
        muscle_uptake = (c.V_MAX_M * C_P) / (c.K_M_M + C_P)
        # muscle_uptake *= (1 - X_M / Cr_max)                               # Too much of a slow down when getting closer to saturation
        muscle_uptake *= (1 - (X_M / CR_MAX) ** 1.5)
        dXAdt = - absorption
        # renal_clearance = 8                                               # Renal clearance [L/h], possibly add when 80% saturation
        # dXPdt = absorption - k_e * X_P - muscle_uptake - renal_clearance * C_P
        dXPdt = absorption - c.k_e * X_P - muscle_uptake
        dXMdt = muscle_uptake - c.k_loss * X_M
        return [dXAdt, dXPdt, dXMdt]

    intervals = range(1, int(TIME_END) + 1)
    concatenated_solution = []
    concatenated_time = []

    for interval in intervals:
        t = np.linspace((interval-1)*TIME_BETWEEN_DOSING, interval*TIME_BETWEEN_DOSING, 1000)
        if interval <= LOADING_END:
            dose = LOADING_DOSE
        else:
            dose = KEEPING_DOSE
        if interval == 1:
            S_0 = [X_A_0, X_P_0, X_M_0]
        else:
            S_0 = [X_A_current[-1] + dose + c.DOSE_DAILY_FOOD, X_P_current[-1], X_M_current[-1]]
        solution = odeint(creatine_model, y0=S_0, t=t)
        X_A_current, X_P_current, X_M_current = solution.T

        concatenated_time += list(t)
        concatenated_solution += list(zip(X_A_current, X_P_current, X_M_current))

    concatenated_time = np.array(concatenated_time)
    concatenated_solution = np.array(concatenated_solution)
    X_A_sol, X_P_sol, X_M_sol = concatenated_solution.T

    C_M = X_M_sol / (c.MW_CR * M_ALL_MUSCLES_KG)                             # Creatine concentration in muscles [mmol/kg]

    return concatenated_time, concatenated_solution, M_ALL_MUSCLES_KG, C_M[-1]

def visualize(TIME, SOLUTION):
    pass

    # print(f"All dry muscles in kg: {M_ALL_MUSCLES_KG}")
    # print(f"Initial amount of creatine: {X_M_0}")

# Previous graphs
# plt.title('Multiple Doses Creatine Intake')
# plt.plot(concatenated_time, X_A_sol, label='Gut (X_A)')
# plt.plot(concatenated_time, X_P_sol, label='Plasma amount (X_P)')
# plt.plot(concatenated_time, X_M_sol, label='Muscle amount (X_M)')
# plt.legend()
# plt.xlabel('Time [h]')
# plt.ylabel('Creatine Amount [mg]')


# plt.plot(concatenated_time, C_M, label='Creatine Concentration')
# plt.xlabel('Time [h]')
# plt.ylabel('Creatine Concentration C_M [mmol.kg-1]')
# plt.title("Creatine Concentration in Muscle")
# # plt.legend()
# plt.show()

def main():
    pass

if __name__ == "__main__":
    main()
