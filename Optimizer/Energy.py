import numpy as np

class Energy:
    """ Object containing the information about any sort of energy production (+) or consumption (-)"""
    def __init__(self,name, energyfunction=1):
        #could contain more information
        self.name = name
        self.energyfunction = energyfunction
        
        return

    
    def setTimedependence(self, timedep_array):
        self.timedep_array = timedep_array
        return
