# Definition of constants and parameters

import numpy as np

V_MAX = 3846                       # Maximum gut absorption rate [mg/h]
K_M = 874                          # Michaelis-Menten constant for absorption to plasma [mg/L]
V_D = 27                           # Apparent volume of distribution [L]; in literature 37 -> 27 to better suit model 
CL = 15                            # Plasma clearance [L/h]; in literature 9.07 -> 15 to better suit model 
k_e = CL / V_D                     # Plasma elimination rate [/h]
K_M_M = 74                         # Michaelis-Menten constant for absorption to muscle [mg/L]
k_loss = np.log(2) / (40*24)       # Muscle loss rate constant (degradation + leakage) [/h]
V_MAX_M = 10000                    # Maximum muscle uptake rate [mg/h], in literature just 1-3 g/h -> 10 g/h
DOSE_DAILY_FOOD = 1500             # Daily dose of creatine [mg]
DRY_FRACTION = 0.25                # Dry fraction of wet muscle mass [/]
C_M_0 = 110                        # Baseline concentration of creatine [mmol/kg dry]
CR_MAX_PER_KG = 150                # Maximum creatine muscle capacity concentration for kg of dry muscle tissue [mmol/kg dry]
MW_CR = 131.13                     # Molecular weight of creatine [mg/mmol]