import pandas as pd 
from datetime import datetime
import requests
import json




def Write_GlobalTimeSeries():
	confirm = pd.read_csv('data/time_series_covid19_confirmed_global.csv')
	deaths = pd.read_csv('data/time_series_covid19_deaths_global.csv')
	recovered = pd.read_csv('data/time_series_covid19_recovered_global.csv')
	cordinates = recovered[['Country/Region','Lat','Long']]

	del confirm['Province/State']
	del deaths['Province/State']
	del recovered['Province/State']
	del confirm['Lat']
	del deaths['Lat']
	del recovered['Lat']
	del confirm['Long']
	del deaths['Long']
	del recovered['Long']

	confirm = confirm.groupby(['Country/Region']).sum()
	deaths = deaths.groupby(['Country/Region']).sum()
	recovered = recovered.groupby(['Country/Region']).sum()
	cordinates = cordinates.groupby(['Country/Region']).mean()

	dateinfo = []

	for r in confirm:
		confirm.rename(columns = {r:r.replace('/','-')}, inplace = True)
		dateinfo.append(r.replace('/','-'));

	for r in recovered:
		recovered.rename(columns = {r:r.replace('/','-')}, inplace = True)

	for r in deaths:
		deaths.rename(columns = {r:r.replace('/','-')}, inplace = True)

	for r in cordinates:
		cordinates.rename(columns = {r:r.replace('/','-')}, inplace = True)


	confirm.to_json('data/confirm.json',orient='index')
	deaths.to_json('data/deaths.json',orient='index')
	recovered.to_json('data/recovered.json',orient='index')
	cordinates.to_json('data/cordinates.json',orient='index')

	with open('data/dateinfo.json', 'w') as outfile:
		json.dump(str(dateinfo), outfile)


def Write_timeline():
	url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india_timeline"
	headers = {
		'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
		'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
		}
	response = requests.request("GET", url, headers=headers)

	
	with open('data/timeline.json', 'w') as outfile:
		json.dump(response.text, outfile)



def Write_districtWise():
	url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"
	headers = {
		'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
		'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
		}
	response = requests.request("GET", url, headers=headers).json()

	with open('data/districtWise.json', 'w') as outfile:
		json.dump(response, outfile)


def retTimeSeries():
	with open('data/timeline.json', "r") as read_file:
		data = json.load(read_file)

	return data

def retDistrictData():
	with open('data/districtWise.json', "r") as read_file:
		data = json.load(read_file)

	return data



def writeFinal_GlobalTimeSeriesData():
	confirm = {}
	recovered = {}
	deaths = {}
	cordinates = {}
	with open('data/confirm.json', "r") as read_file:
		confirm = json.load(read_file)

	with open('data/recovered.json', "r") as read_file:
		recovered = json.load(read_file)

	with open('data/deaths.json', "r") as read_file:
		deaths = json.load(read_file)

	with open('data/cordinates.json', "r") as read_file:
		cordinates = json.load(read_file)

	combined_dict = {}
	
	for country in cordinates:
		tmp = {}
		for dte in confirm[country]:
			tmp[dte] = {
							'confirm':confirm[country][dte],
							'deaths':deaths[country][dte],
							'recovered':recovered[country][dte],
						}
		combined_dict[country] = {
				'Lat': cordinates[country]['Lat'],
				'Long':cordinates[country]['Long'],
				'country-name':country,
				'data':tmp
		}

	with open('data/global_timeline.json', 'w') as outfile:
		json.dump(combined_dict, outfile)


def retGlobalTimeSeriesData():
	with open('data/global_timeline.json', "r") as read_file:
		data = json.load(read_file)

	return data


def retDateinfo():
	with open('data/dateinfo.json', "r") as read_file:
		data = json.load(read_file)

	return data



def Write_Globaldata():
	url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
	querystring = {"country":"Canada"}
	headers = {
		'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
		'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
		}
	page = requests.request("GET", url, headers=headers).json()
	with open('data/Global_data.json', 'w') as outfile:
		json.dump(page, outfile)



def retGlobaldata():
	with open('data/Global_data.json', "r") as read_file:
		data = json.load(read_file)

	return data





def Write():
	Write_timeline()
	Write_districtWise()
	Write_GlobalTimeSeries()
	writeFinal_GlobalTimeSeriesData()
	Write_Globaldata()
#Write()
