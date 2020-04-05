import pandas as pd 
from datetime import datetime


def retTimeSeries():

	timeseriesData = {}
	confirm = pd.read_csv('data/time_series_covid19_confirmed_global.csv')
	deaths = pd.read_csv('data/time_series_covid19_deaths_global.csv')
	recovered = pd.read_csv('data/time_series_covid19_recovered_global.csv')
	confirm = confirm.loc[confirm['Country/Region'] == 'India']
	deaths = deaths.loc[deaths['Country/Region'] == 'India']
	recovered = recovered.loc[recovered['Country/Region'] == 'India']
	confirm = confirm.drop(['Province/State','Lat','Long','Country/Region'], axis=1)
	deaths = deaths.drop(['Province/State','Lat','Long','Country/Region'], axis=1)
	recovered = recovered.drop(['Province/State','Lat','Long','Country/Region'], axis=1)

	con = {}
	for col1 in confirm:
		date_str = ""+col1+"20"
		key = datetime.strptime(date_str, '%m/%d/%Y').date()		
		con[str(key)] = {'confirmed':confirm[col1].tolist()[0],'deaths':deaths[col1].tolist()[0],'recovered':recovered[col1].tolist()[0]}

	timeseriesData['data'] = con

	return timeseriesData
