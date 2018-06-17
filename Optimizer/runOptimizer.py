from scipy import optimize
import numpy as np
from Optimize import Optimize
from Appliance import Appliance
from Surplus import Surplus
import matplotlib.pyplot as plt 




#components: prediction (constraint), human behaviour (constraint), appliances, battery
#minimize: Energy surplus

#fromiter(iterable, dtype[, count]) 	Create a new 1-dimensional array from an iterable object.

appliance_list = []
#create the appliances
washing_machine = Appliance("washing_machine", 3, 2.5)
appliance_list.append(washing_machine)
cleaning_robot = Appliance("cleaning_robot", 4, 1.3)
appliance_list.append(cleaning_robot)


surplus = Surplus("Example House")
surplus_pred = surplus.Surplus_predicted()
#func_Surplus_predicted()

Opt_app1 = Optimize(washing_machine)
Opt_app2 = Optimize(cleaning_robot)
Opt_app1.Optimize_start_time(surplus_pred)
surplus2 = surplus.RecalculateSurplus(surplus_pred, washing_machine.TimeDep_fromStartTime(Opt_app1.first_good_starting_time), state="with washing machine", appliance=washing_machine.TimeDep_fromStartTime(Opt_app1.first_good_starting_time) )



print("Optimal time to start the {} is at {}h".format( Opt_app1.appliance.name,Opt_app1.first_good_starting_time))
Opt_app2.Optimize_start_time(surplus2)
surplus_pred_wash = Surplus()
surplus_pred_wash.setSurplus( surplus2 )


surplus_optimized = surplus_pred_wash.RecalculateSurplus(surplus2, cleaning_robot.TimeDep_fromStartTime(Opt_app2.first_good_starting_time), state="with cleaning robot", appliance=cleaning_robot.TimeDep_fromStartTime(Opt_app2.first_good_starting_time) )
print("Optimal time to start the {} is at {}h".format( Opt_app2.appliance.name,Opt_app2.first_good_starting_time))

x=np.arange(24)

optimized = plt.step(x,surplus_optimized,label="all appliances")
with_washing_machine = plt.step(x,surplus2,label="washing")
before = plt.step(x,surplus_pred,label="before")



plt.legend()
plt.show()
