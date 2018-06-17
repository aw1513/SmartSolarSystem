import numpy as np
import pandas as pd
from weather_predictor import WeatherPredictor

class Load():
	def __init__(self, power, duration):
		self.power = power
		self.T = duration

		self.started = False
		self.t = 0 		# already completed step
		self.finished = False

	def run(self):
		# run the load and return power
		self.t += 1
		if self.t == self.T:
			self.finished = True
		return self.power

class Optimizer():
	def __init__(self, loads):
		self.loads = loads

	def get_consumption(self):
		consumption = 0
		for load in loads:
			if load.started and not load.finished:
				consumption += load.run()

		return consumption

	def optimize(self, energy_surplus):

		started_var_loads = np.zeros(len(energy_surplus))
		for load in loads:
			if load.started and not load.finished:
				time_left = load.T - load.t
				started_var_loads[ : time_left ] += load.power  # add power of already running loads to fixed part!

		energy_surplus = energy_surplus - started_var_loads

		# ----------------

		predicted_var_loads = energy_surplus # DUMMY!!

		# -------------------

		## find the earliest possible date to run one load, start with the biggest load
		# ONLY OPTIMIZE FOR ELEMENTS WHERE START = FALSE
		## if the earliest start time is at t = 0, set load.started to TRUE!
		# return variable load prediction
		return predicted_var_loads

class SmartHome():

	def __init__(self, battery_capacity, battery_power, variable_loads, base_load, weather_data, train_date):
		# initialize weather predictor
		self.WEATHER_TARGET  = 'power_output_noisy'
		self.WEATHER_FEATURES = ['sunshine_dur', 'precipitation', 'GHI', 'temp', 'apparent_zenith', 'azimuth']
		self.setup_predictor(weather_data, train_date)

		# initialize battery
		self.battery_soc = 0.5 # initialize the state-of-charge of the battery
		self.battery_capacity = battery_capacity
		self.battery_power = battery_power

		# initialize optimizer
		self.var_load_optimizer = Optimizer(variable_loads)

		# initialize base_load
		BASELOAD_NOISE_LEVEL = 0.25		# noise level in %
		self.setup_baseload(base_load, BASELOAD_NOISE_LEVEL)

	def setup_predictor(self, all_data, train_end, evaluate = True):
		self.historical_weather = all_data[:train_end]
		self.predicted_weather = all_data[train_end:]

		mypred = WeatherPredictor(n_estimators = 1000, max_features = 0.5)
		mypred.fit_model(historical_weather, self.WEATHER_FEATURES, self.WEATHER_TARGET)
		
		if evaluate: mypred.evaluate_estimator()

	def setup_baseload(self, base_load, noise_level):
		self.base_load = base_load
		load_noise = [np.random.normal(0,noise_level*p,1) for p in base_load.power]
		base_load['load_noise'] = np.asarray(load_noise)
		self.base_load_prediction = np.maximum(base_load.power + base_load.load_noise, 0)


############## LIVE PERFORMANCE OF THE SMART HOME ##############################

	def update(self, timestamp):

		# evaluate_current_timestamp:
		PV_production = self.get_weather_measurement(timestamp)
		base_consumption = self.get_baseload_measurement(timestamp)
		variable_consumption = self.var_load_optimizer.get_consumption()

		energy_surplus = PV_production - base_consumption - variable_consumption
		battery_usage = self.update_battery(energy_surplus)

		self_consumption = min(PV_production, base_consumption + variable_consumption + battery_usage)

		# predict for next timestamp:
		predicted_production = self.predict_weather(timestamp)
		predicted_baseload = self.predict_baseload(timestamp)

		predicted_surplus = predicted_production - predicted_baseload
		predicted_var_load = self.var_load_optimizer.optimize(predicted_surplus)

		return {'PV_production'			: PV_production, 
				'base_consumption'		: base_consumption,
				'variable_consumption'	: variable_consumption,
				'battery_usage'			: battery_usage,
				'self_consumption'		: self_consumption, 
				'predicted_production'	: predicted_production,
				'predicted_baseload'	: predicted_baseload,
				'predicted_var_load' 	: predicted_var_load, 
				}


	def update_battery(self, energy_surplus):
		# positive energy surplus: battery should be charged
		# negative energy 'surplus': battery is discharged

		if energy_surplus > 0 and self.battery_soc < 1:
			# charge battery:
			available_capacity = self.battery_capacity * (1-self.battery_soc)
			new_energy = min(energy_surplus, self.battery_power) # we can never charge more than the maximum charging power in 1h!
			stored_energy =  min(new_energy, available_capacity)
			self.battery_soc += stored_energy / self.battery_capacity

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

			if self.battery_soc < 0:
				print('WARINING: battery state of charge is less than 0! (%f)' %self.battery_soc)

		return 0		# if no energy is consumed, 0 is returned (no positive effect on the self-consumption balance)

	def get_weather_measurement(self, timestamp):
		return self.predicted_weather[timestamp][self.WEATHER_TARGET]

	def get_baseload_measurement(self, timestamp):
		return self.base_load_prediction[timestamp]
	

	def predict_weather(self, timestamp, prediction_horizon = 24):
		# prediction_horizon: horizon in hours
		predict_start = timestamp
		predict_end = timestamp + pd.to_timedelta(prediction_horizon-1, unit = 'h')
		
		new_data = self.predicted_weather[predict_start:predict_end] # this comes from the weather station!

		return mypred.predict(new_data, self.WEATHER_FEATURES) 


	def predict_baseload(self, timestamp, prediction_horizon = 24):
		# prediction_horizon: horizon in hours
		predict_start = timestamp
		predict_end = timestamp + pd.to_timedelta(prediction_horizon-1, unit = 'h')
		
		return self.base_load_prediction[predict_start:predict_end] # this comes from the weather station!