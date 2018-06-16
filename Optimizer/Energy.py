import numpy as np

class Energy:
    """ Object containing the information about any sort of energy production (+) or consumption (-)"""
    def __init__(self,name, energy=0):
        #could contain more information
        self.name = name
        self.energy = energy
        
        return
