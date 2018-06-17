import numpy as np
from Appliance import Appliance

class Optimize:
    def __init__(self , appliance):
        self.appliance = appliance

        self.starting_time = -9
        self.surplus = 0
        return


    def Optimize_start_time(self, surplus_array_orig):
        #good_starting_times = []
        #loop through the possible starting times
        #calculate the surplus for each of them
        first_good_starting_time = -9
        surplus = 999999
        appliance = self.appliance
        
        for t in range(len(appliance.possible_starting_times)):
            #print("time in optim {}".format(t))
            appliance_array = appliance.TimeDep_fromStartTime(t)
            #print(appliance_array)
            #print(len(appliance_array))
            #surplus array must be the original one again!!!
            #print("before {} {}".format(surplus_array_orig, appliance_array))
            surplus_array = surplus_array_orig - appliance_array
            #print("after {}".format(surplus_array))
            surplus_t = sum(abs(surplus_array))
            #print(t,surplus_t)
            if abs(surplus_t) < surplus:
                #print(surplus_t)
                surplus = surplus_t
                first_good_starting_time = t

        self.surplus = surplus
        self.first_good_starting_time = first_good_starting_time
        return { appliance.name:
                 {"surplus": surplus,
                  "first_good_starting_time": first_good_starting_time
                 }}
