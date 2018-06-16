from scipy import optimize
import numpy as np
from Energy import Energy

import matplotlib.pyplot as plt 

#components: prediction (constraint), human behaviour (constraint), appliances, battery
#minimize: Energy surplus

#fromiter(iterable, dtype[, count]) 	Create a new 1-dimensional array from an iterable object.

def func_Surplus_day(t):
    """ Surplus energy in dependence of a certain amount of parameters like starting times """
    

    energyproduction = np.array( [ 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 6,8,9,8,7,6,6,5,4,2,0,0,0, 0 ] )

    energyconsumption = np.array  ( [0.4,0.25,0.2,0.07,0.07,0.07,0.08,0.2,0.6,0.6,0.5,0.5,0.5,0.5,0.5,0.5,0.6,0.6,0.7,0.9,1.0,1.0,0.9,0.8])

    #t is starting time: the index of the bin where it starts to be a certain value
    #array i
    #print((t[0]))
    optimizable_appliance = np.zeros(24)

    optimizable_appliance[t:t+3] = 0.5

    surplus = energyproduction - energyconsumption- optimizable_appliance
    
    return sum(abs(surplus))

#since we know that the optimal hour will be one of 24, can just loop over them without needing complex optimization

times = np.arange(24-2)

surplus = 9999
index = -9

for t in times:

    surplus_t = func_Surplus_day(t)
    print(t,surplus_t)
    if abs(surplus_t) < surplus:
        surplus = surplus_t
        index = t

indexlist =[]
for t in times:
    surplus_t = func_Surplus_day(t)
    if abs(surplus_t) == surplus:
        indexlist.append(t)


print("Minimum surplus = {} for starting the appliance between {}h and {}h ".format(surplus,indexlist[0], indexlist[len(indexlist)-1]))

#time_guess = np.array([1])

#res = optimize.minimize(func_Surplus_day, time_guess, method='nelder-mead',  options={'xtol': 1e-8, 'disp': True})
#print(res.x)

