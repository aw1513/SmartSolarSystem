import numpy as np

class Surplus:
    def __init__(self,name="Surplus"):
        self.name = name
        self.surplus = 0
        return

    def Surplus_predicted(self):
        """ Surplus energy in dependence of a certain amount of parameters like starting times """
        
        energyproduction = np.array( [ 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 6,8,9,8,7,6,6,5,4,2,0,0,0, 0 ] )
        energyconsumption = np.array  ( [0.4,0.25,0.2,0.07,0.07,0.07,0.08,0.2,0.6,0.6,0.5,0.5,0.5,0.5,0.5,0.5,0.6,0.6,0.7,0.9,1.0,1.0,0.9,0.8])
        
        
        surplus = energyproduction - energyconsumption 
        self.surplus = surplus
        return surplus
    def setSurplus(self,surplus):
        self.surplus = surplus
        return

    def setState(self,state):
        self.state = state
        return

    def RecalculateSurplus(self, before, after,state, appliance=np.zeros(24)):

        after = before-appliance
        self.setState = state
        return after
