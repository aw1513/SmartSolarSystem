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
    print((t[0]))
    before_t0 = np.zeros(int(t[0]))
    during_appliance = np.array([0.5,0.5,0.5])
    after_t0plus3 = np.zeros(24-int(t[0])-3)
    #print(type(before_t0), type(during_appliance), type(after_t0plus3))
    #print(before_t0, during_appliance, after_t0plus3)
    
    o_1 = np.append(before_t0,during_appliance) #,after_t0plus3)
    optimizable_appliance = np.append( o_1 ,after_t0plus3)
    #print(t[0])
    #print(optimizable_appliance)
    
    #surplus = energyproduction - energyconsumption - optimizable_appliance
    surplus = energyproduction - energyconsumption- optimizable_appliance
    #print(abs(surplus))
    print(sum(abs(surplus)))
    
    return sum(abs(surplus))
time_guess = np.array([3])

#res = optimize.minimize(func_Surplus_day, time_guess, method='nelder-mead',  options={'xtol': 1e-8, 'disp': True})
res = optimize.minimize(func_Surplus_day, time_guess, method='nelder-mead',  options={'xtol': 0.5, 'disp': True})
print(res.x)


#
#
#
##time
#time = np.linspace(0, 24, 24)   # start, end, num-points
##actually, this should be done in datetime
#
#
#
#
#
#
#
##prediction of energy input
#def f_energyproduction(t):
#    return  np.array([ - 3*(t[0]-4)**2 +20])
#energyproduction = Energy("production", f_energyproduction) #(time))
##print(f_energyproduction)
##plt.plot(time, f_energyproduction, 'o')  # dot plot
#
##fixed energy consumption
#def f_energyconsumption(t):
#    return np.array([ t[0]**2- t[0]**4])
#energyconsumption = Energy("consumption_fixed", f_energyconsumption) #(time))
#
##appliance_1 = Energy("washing_machine")
##def wash(t):
##    return t
##appliance.setTimedependence()
#
#surplus = energyproduction.energy(time) - energyconsumption.energy(time)
#E_surplus = Energy("surplus", surplus)
#
#print(surplus)
#
##def appliances(t):
##    return np.array(  [   ]  )
#
#time = np.linspace(0, 24, 24*6)   # start, end, num-points
#
##res = optimize.minimize(energyconsumption, time)
##res = optimize.minimize(energyproduction.energy, time)
#res = optimize.minimize(surplus, time)
#print(res)
