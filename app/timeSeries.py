import pandas as pd 



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
	dea = {}
	rec = {}
	for col in confirm:
	    con[col+"20"] = confirm[col].tolist()[0]
	for col in deaths:
	    dea[col+"20"] = deaths[col].tolist()[0]
	for col in recovered:
	    rec[col+"20"] = recovered[col].tolist()[0]

	timeseriesData['confirmed'] = con
	timeseriesData['deaths'] = dea
	timeseriesData['recovered'] = rec

	return timeseriesData
