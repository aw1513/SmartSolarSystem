import numpy as np

class Appliance:

    def __init__(self, name,duration,power_per_hour):

        #don't start after 24-length
        self.name = name
        self.duration = duration
        self.total_power = duration*power_per_hour
        self.power_per_hour = power_per_hour
        self.possible_starting_times = np.zeros(24-self.duration-1)
        #sum(self.timedependence)
        #to order the appliances
            
        return
    
    def TimeDep_fromStartTime(self,start_time):
        start_time = start_time

        appliance =  np.zeros(24-self.duration)
        #self.possible_starting_times
        #print("a")
        #print(appliance)
        #print(start_time)
        appliance[start_time:start_time+self.duration] = self.power_per_hour
        #if the array is shorter than start_time+duration, need to extend it
        if len(appliance)<start_time+self.duration:
            n = start_time+self.duration-len(appliance)
            #print(n)
            additional_appl = np.full(n, self.power_per_hour)
            appliance = np.append(appliance, additional_appl)

        #print(appliance)
        additional_zeros = np.zeros(24- len(appliance))
        #print(len(appliance), additional_zeros)
        appliance_day = np.append(appliance,additional_zeros)
        self.time_dependence = appliance_day
        #print(appliance_day)
        return appliance_day

