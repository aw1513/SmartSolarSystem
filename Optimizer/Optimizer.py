from scipy import optimize
import numpy as np
from Optimize import Optimize
from Appliance import Appliance
import matplotlib.pyplot as plt 




#components: prediction (constraint), human behaviour (constraint), appliances, battery
#minimize: Energy surplus

#fromiter(iterable, dtype[, count]) 	Create a new 1-dimensional array from an iterable object.


def func_Surplus_predicted(appliance=np.zeros(24)):
    """ Surplus energy in dependence of a certain amount of parameters like starting times """

    energyproduction = np.array( [ 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 6,8,9,8,7,6,6,5,4,2,0,0,0, 0 ] )
    energyconsumption = np.array  ( [0.4,0.25,0.2,0.07,0.07,0.07,0.08,0.2,0.6,0.6,0.5,0.5,0.5,0.5,0.5,0.5,0.6,0.6,0.7,0.9,1.0,1.0,0.9,0.8])

    #t is starting time: the index of the bin where it starts to be a certain value
    #array i
    #print((t[0]))
    #optimizable_appliance = np.zeros(24)

    #    optimizable_appliance[t:t+3] = 0.5
    

    surplus = energyproduction - energyconsumption - appliance
    
    #return sum(abs(surplus))
    return surplus




#create the appliances
washing_machine = Appliance("washing_machine", 3, 0.5)
cleaning_robot = Appliance("cleaning_robot", 4, 0.3)
surp = func_Surplus_predicted()

Opt_app1 = Optimize(washing_machine)

Opt_app2 = Optimize(cleaning_robot)
Opt_app1.Optimize_start_time(surp)

washing_machine_new = washing_machine.TimeDep_fromStartTime(Opt_app1.first_good_starting_time)

surplus2 = func_Surplus_predicted( washing_machine_new )
print("Optimal time to start the {} is at {}h".format( Opt_app1.appliance.name,Opt_app1.first_good_starting_time))
Opt_app2.Optimize_start_time(surplus2)

print("Optimal time to start the {} is at {}h".format( Opt_app2.appliance.name,Opt_app2.first_good_starting_time))
