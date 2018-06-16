from scipy import optimize
import numpy as np
from Energy import Energy

import matplotlib.pyplot as plt 

#components: prediction (constraint), human behaviour (constraint), appliances, battery
#minimize: Energy surplus

#time
time = np.linspace(0, 24, 24*6)   # start, end, num-points
#actually, this should be done in datetime

#prediction of energy input
def f_energyproduction(t):
    return  np.array([ - 3*(t[0]-4)**2 +20])
energyproduction = Energy("production", f_energyproduction)
#print(f_energyproduction)
#plt.plot(time, f_energyproduction, 'o')  # dot plot

#fixed energy consumption
def f_energyconsumption(t):
    return np.array([ t[0]**2- t[0]**4])
energyconsumption = Energy("consumption_fixed", f_energyconsumption)

#appliance_1 = Energy("washing_machine")
#def wash(t):
#    return t
#appliance.setTimedependence()


#def appliances(t):
#    return np.array(  [   ]  )

time = np.linspace(0, 24, 24*6)   # start, end, num-points

res = optimize.minimize(energyproduction.energyfunction, time)
print(res)
