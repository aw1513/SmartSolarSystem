import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor as RF 
import matplotlib
import matplotlib.pyplot as plt 
from sklearn.metrics import mean_squared_error as mse
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

def discrete_cmap(N, base_cmap='hsv'):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    m = round(N/2)-1
    color_list = np.concatenate([color_list[m::-1],color_list[:m:-1]])
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

class WeatherPredictor():

	def __init__(self, n_estimators, max_features, n_jobs = -1, warm_start = False):
		self.estimator = RF( n_estimators = n_estimators, 
							 max_features=max_features, 
							 n_jobs = n_jobs, warm_start = warm_start)

	def fit_model(self, weather_frame, feature_columns, target_columns, val_ratio = 0.2):

		targets = weather_frame.loc[:,target_columns].values
		features = weather_frame.loc[:,feature_columns].values

		train_ftrs, self.test_ftrs, train_tgts, self.test_tgts = train_test_split(features, targets, test_size=val_ratio)
		self.normalize = lambda x: (x - np.mean(train_tgts)) / np.std(train_tgts)
		
		self.estimator.fit(train_ftrs, train_tgts)

	def evaluate_estimator(self, lim = 6500):

		# create test prediction:
		test_pred = self.estimator.predict(self.test_ftrs)

		self.mse = mse(self.normalize(test_pred), self.normalize(self.test_tgts))

		X = test_pred.reshape((-1,1))
		Y = self.test_tgts.reshape((-1,1))
		linX = np.linspace(0,lim,lim).reshape(-1, 1)

		model = LinearRegression()
		model.fit(X, Y)
		linY = model.predict(linX)

		coef = model.coef_
		intcpt = model.intercept_
		R2 = model.score(X, Y)

		plt.figure(figsize = (7,5.5))
		matplotlib.rcParams.update({'font.size': 15}) 
		plt.plot(linX,linY, 'k', LineWidth = 1.5)
		plt.scatter(test_pred, self.test_tgts, s=3) #, norm=norm)
		plt.ylabel('Targets (in $W$)')
		plt.xlabel('Prediction (in $W$)')
		# plt.axis('equal')
		plt.ylim(0, lim)
		plt.xlim(0, lim)
		plt.text(100, 6500, ("$R^2$ = %.3f\ny = %.5f x - %.3f" %(R2, coef, abs(intcpt))) )
		plt.title('Distribution of targets and prediction for test data')
		plt.show()

		return self.mse

	def predict(self, weather_frame, feature_columns):

		return self.estimator.predict(weather_frame.loc[:,feature_columns].values)

	def save(self, filename):
		joblib.dump(self.estimator, filename)

#	def add_data(weather_file, new_row):



