import numpy as np
import pandas as pd
from weather_predictor import WeatherPredictor
import csv
from scipy import optimize
# from Optimize import Optimize

def write_row_to_csv( filename, content_vector, initialize = False ):
    # writes a row to a csv file
    if initialize:  open_mode = 'w'
    else:           open_mode = 'a'

    with open(filename, open_mode) as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        w.writerow( content_vector )

class Load():
    def __init__(self, power, duration, name, prediction_horizon = 24):
        self.duration = duration
        self.total_power = duration*power
        self.power_per_hour = power

        self.started = False
        self.t = 0      # already completed step
        self.finished = False

        self.name = name
        self.possible_starting_times = np.zeros(prediction_horizon-self.duration-1)
        self.prediction_horizon = prediction_horizon

    def run(self):
        # run the load and return power
        self.started = True
        if not self.finished:
            self.t += 1
            if self.t == self.duration:
                self.finished = True
            return self.power_per_hour
        return 0

    def TimeDep_fromStartTime(self,start_time):
        start_time = start_time

        appliance =  np.zeros(self.prediction_horizon)
        #self.possible_starting_times
        #print("a")
        #print(appliance)
        #print(start_time)
        end_time = min(start_time+self.duration, self.prediction_horizon)
        if start_time+self.duration > self.prediction_horizon:
            print('WARNING: something is wrong when calculating possible starting times')
        
        appliance[start_time:end_time] = self.power_per_hour
        # #if the array is shorter than start_time+duration, need to extend it
        # if len(appliance)<start_time+self.duration:
        #     n = start_time+self.duration-len(appliance)
        #     #print(n)
        #     additional_appl = np.full(n, self.power_per_hour)
        #     appliance = np.append(appliance, additional_appl)

        # #print(appliance)
        # additional_zeros = np.zeros(24- len(appliance))
        #print(len(appliance), additional_zeros)
        # appliance_day = np.append(appliance,additional_zeros)
        appliance_day = appliance
        self.time_dependence = appliance_day
        #print(appliance_day)
        return appliance_day

########################################################

class Optimizer():
    def __init__(self, loads):
        self.loads = loads

    def get_consumption(self):
        consumption = 0
        for load in self.loads:
            if load.started and not load.finished:
                consumption += load.run()

        return consumption

    def optimize(self, energy_surplus):

        started_var_loads = np.zeros(len(energy_surplus))
        for load in self.loads:
            if load.started and not load.finished:
                time_left = load.duration - load.t
                started_var_loads[ : time_left ] += load.power_per_hour  # add power of already running loads to fixed part!

        energy_surplus = energy_surplus - started_var_loads

        # ----------------

        predicted_loads_timeseries = np.zeros(len(energy_surplus))

        for appliance in self.loads:
            if not appliance.started:
                Opt_app = Optimize(appliance)  # declare optimizer
                Opt_app.Optimize_start_time(energy_surplus)

                new_load_timeseries = appliance.TimeDep_fromStartTime(Opt_app.first_good_starting_time)
                energy_surplus = energy_surplus - new_load_timeseries

                predicted_loads_timeseries += new_load_timeseries
                
                if Opt_app.first_good_starting_time <= 1:
                    appliance.started = True

        # -------------------

        ## find the earliest possible date to run one load, start with the biggest load
        # ONLY OPTIMIZE FOR ELEMENTS WHERE START = FALSE
        ## if the earliest start time is at t = 0, set load.started to TRUE!
        # return variable load prediction
        return predicted_loads_timeseries

##########################################

class Optimize():
    def __init__(self , appliance):
        self.appliance = appliance

        self.starting_time = -9
        self.surplus = 0


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

##################################################

class SmartHome():

    def __init__(self, battery_capacity, battery_power, variable_loads, base_load, weather_data, train_date, log_name):
        # initialize weather predictor
        self.WEATHER_TARGET  = 'power_output_noisy'
        self.WEATHER_FEATURES = ['sunshine_dur', 'precipitation', 'GHI', 'temp', 'apparent_zenith', 'azimuth']
        self.setup_predictor(weather_data, train_date)
        print('set up and trained weather predictor with data up to ', train_date)

        # initialize battery
        self.battery_soc = 0.3 # initialize the state-of-charge of the battery
        self.battery_capacity = battery_capacity
        self.battery_power = battery_power
        print('set up battery with capacity %.2f and maximum power %.2f' %(battery_capacity, battery_power))

        # initialize optimizer
        self.var_load_optimizer = Optimizer(variable_loads)
        print('set up variable load optimizer')

        # initialize base_load
        BASELOAD_NOISE_LEVEL = 0.25     # noise level in %
        self.setup_baseload(base_load, BASELOAD_NOISE_LEVEL)
        print('set up base load')

        # initialize logger
        self.log_name = log_name
        write_row_to_csv( self.log_name, 
                          ['timestamp', 'PV_production', 'base_consumption', 'var_consumption', 'battery_consumption', 'self_consumption'], 
                          initialize = True )

        # set up current token value
        self.last_timestamp = train_date
        self.curr_token = 0

    def setup_predictor(self, all_data, train_end, evaluate = True):
        historical_weather = all_data[:train_end]
        self.predicted_weather = all_data[train_end:]

        self.PV_predictor = WeatherPredictor(n_estimators = 1000, max_features = 0.5)
        self.PV_predictor .fit_model(historical_weather, self.WEATHER_FEATURES, self.WEATHER_TARGET)
        
        if evaluate: self.PV_predictor .evaluate_estimator()

    def setup_baseload(self, base_load, noise_level):
        self.base_load = base_load
        load_noise = [np.random.normal(0,noise_level*p,1) for p in base_load.power]
        base_load['load_noise'] = np.asarray(load_noise)
        self.base_load_prediction = np.maximum(base_load.power + base_load.load_noise, 0)


############## LIVE PERFORMANCE OF THE SMART HOME ##############################

    def update(self, timestamp):

        try:
            if pd.to_datetime(self.last_timestamp).date() != pd.to_datetime(timestamp).date():
                self.curr_token = 0
                print('resetted current token')

            # evaluate_current_timestamp:
            PV_production = self.get_weather_measurement(timestamp)
            base_consumption = self.get_baseload_measurement(timestamp)
            variable_consumption = self.var_load_optimizer.get_consumption()
            print('current PV production: %.2fkWh' %PV_production)
            print('current base consumption: %.2fkWh' %base_consumption)
            print('current variable consumption: %.2fkWh' %variable_consumption)

            energy_surplus = PV_production - base_consumption - variable_consumption
            battery_usage = self.update_battery(energy_surplus)
            print('current battery usage: %.2fkWh' %battery_usage)

            self_consumption = min(PV_production, base_consumption + variable_consumption + battery_usage)
            print('total self consumption: %.2fkWh' %self_consumption)

            self.curr_token = self.curr_token + self_consumption
            print('new token value for today: %.2f' %self.curr_token)
            
            write_row_to_csv( self.log_name, 
                              [timestamp, PV_production, base_consumption, variable_consumption, battery_usage, self_consumption], 
                             )
            # predict for next timestamp:
            predicted_production = self.predict_weather(timestamp)
            predicted_baseload = self.predict_baseload(timestamp)

            predicted_surplus = predicted_production - predicted_baseload
            predicted_var_load = self.var_load_optimizer.optimize(predicted_surplus)

            print('predicted all future loads')

            self.last_timestamp = timestamp

            return {'PV_production'         : PV_production, 
                    'base_consumption'      : base_consumption,
                    'variable_consumption'  : variable_consumption,
                    'battery_usage'         : battery_usage,
                    'self_consumption'      : self_consumption, 
                    'token_value'           : self.curr_token,
                    'predicted_production'  : predicted_production,
                    'predicted_baseload'    : predicted_baseload,
                    'predicted_var_load'    : predicted_var_load, 
                    }

        except:
            print('failed to execute timestamp - skip to next one')
            return 0


    def update_battery(self, energy_surplus):
        # positive energy surplus: battery should be charged
        # negative energy 'surplus': battery is discharged

        if energy_surplus > 0 and self.battery_soc < 1:
            # charge battery:
            available_capacity = self.battery_capacity * (1-self.battery_soc)
            new_energy = min(energy_surplus, self.battery_power) # we can never charge more than the maximum charging power in 1h!
            stored_energy =  min(new_energy, available_capacity)
            self.battery_soc += stored_energy / self.battery_capacity
            print('charge battery; new battery state of charge: %.2f' %self.battery_soc)

            if self.battery_soc > 1:
                print('WARINING: battery state of charge is greater than 1! (%f)' %self.battery_soc)

            return stored_energy

        elif energy_surplus < 0 and self.battery_soc > 0:
            energy_deficit = abs(energy_surplus)
            # discharge battery:
            available_energy = self.battery_capacity * (self.battery_soc)
            usable_energy = min(energy_deficit, self.battery_power) # we can never charge more than the maximum charging power in 1h!
            recovered_energy =  min(available_energy, usable_energy)
            self.battery_soc -= recovered_energy / self.battery_capacity
            print('discharged battery; new battery state of charge: %.2f' %self.battery_soc)

            if self.battery_soc < 0:
                print('WARINING: battery state of charge is less than 0! (%f)' %self.battery_soc)

        return 0        # if no energy is consumed, 0 is returned (no positive effect on the self-consumption balance)

    def get_weather_measurement(self, timestamp):
        return self.predicted_weather.loc[timestamp][self.WEATHER_TARGET]

    def get_baseload_measurement(self, timestamp):
        return self.base_load_prediction.loc[timestamp]
    

    def predict_weather(self, timestamp, prediction_horizon = 24):
        # prediction_horizon: horizon in hours
        predict_start = timestamp
        predict_end = timestamp + pd.to_timedelta(prediction_horizon-1, unit = 'h')
        
        new_data = self.predicted_weather[predict_start:predict_end] # this comes from the weather station!

        return self.PV_predictor .predict(new_data, self.WEATHER_FEATURES) 


    def predict_baseload(self, timestamp, prediction_horizon = 24):
        # prediction_horizon: horizon in hours
        predict_start = timestamp
        predict_end = timestamp + pd.to_timedelta(prediction_horizon-1, unit = 'h')
        
        return self.base_load_prediction[predict_start:predict_end] # this comes from the weather station!