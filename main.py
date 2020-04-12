import flask
import requests
from bs4 import BeautifulSoup
import json

import pandas as pd
from datetime import datetime
import requests
import json



app = flask.Flask(__name__)
app.config["DEBUG"] = True


def Write_GlobalTimeSeries():
	confirm = pd.read_csv('time_series_covid19_confirmed_global.csv')
	deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
	recovered = pd.read_csv('time_series_covid19_recovered_global.csv')
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


	confirm.to_json('confirm.json',orient='index')
	deaths.to_json('deaths.json',orient='index')
	recovered.to_json('recovered.json',orient='index')
	cordinates.to_json('cordinates.json',orient='index')

	with open('dateinfo.json', 'w') as outfile:
		json.dump(str(dateinfo), outfile)


def Write_timeline():
	url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india_timeline"
	headers = {
		'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
		'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
		}
	response = requests.request("GET", url, headers=headers)


	with open('timeline.json', 'w') as outfile:
		json.dump(response.text, outfile)



def Write_districtWise():
	url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"
	headers = {
		'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
		'x-rapidapi-key': "78144a9bd9msh16e7e3bc08ebff0p1d5199jsn8b8bdd31763d"
		}
	response = requests.request("GET", url, headers=headers).json()

	with open('districtWise.json', 'w') as outfile:
		json.dump(response, outfile)


def retTimeSeries():
	with open('timeline.json', "r") as read_file:
		data = json.load(read_file)

	return data

def retDistrictData():
	with open('districtWise.json', "r") as read_file:
		data = json.load(read_file)

	return data



def writeFinal_GlobalTimeSeriesData():
	confirm = {}
	recovered = {}
	deaths = {}
	cordinates = {}
	with open('confirm.json', "r") as read_file:
		confirm = json.load(read_file)

	with open('recovered.json', "r") as read_file:
		recovered = json.load(read_file)

	with open('deaths.json', "r") as read_file:
		deaths = json.load(read_file)

	with open('cordinates.json', "r") as read_file:
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

	with open('global_timeline.json', 'w') as outfile:
		json.dump(combined_dict, outfile)


def retGlobalTimeSeriesData():
	with open('global_timeline.json', "r") as read_file:
		data = json.load(read_file)

	return data


def retDateinfo():
	with open('dateinfo.json', "r") as read_file:
		data = json.load(read_file)

	return data


def Write():
	Write_timeline()
	Write_districtWise()
	Write_GlobalTimeSeries()
	writeFinal_GlobalTimeSeriesData()
#Write()


url = "https://mohfw.gov.in"



def tableData(soup):
	data = {}
	response = {}
	table = soup.find('table', class_='table').find('tbody')
	tab_ = table.find_all('tr');
	time = soup.find('div',class_="status-update").find('span')
	response['update-time'] = time.text
	f = open('table.html','w')
	f.write(str(table))
	f.write(str(time))

	for tr in tab_:
		tds = tr.find_all('td')
		if(len(tds)==5):
			data[tds[1].text] = {
							'Confirmed Cases':tds[2].text,
							'Cured/Discharged':tds[3].text,
							'Deaths':tds[4].text
							}

	response['data'] = data

	with open('State_data.json', 'w') as writer:
		json.dump(response, writer)

	return response

def getUrl(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	return soup



def DistrictLink(soup):

	links = soup.find_all('a')
	link = "-";

	f = open('soup.html','w')
	f.write(str(links))
	for l in links:
		if("District Reportings" in l.text):
			link = l.get('href')
			break;

	return link


def District(soup):
	link = DistrictLink(soup);
	return link




@app.route('/', methods=['GET'])
def home():
	#return tableData();
    return "<h1>Distant Reading Archive</h1>Api for Covid Data for India</p> <li><ui> <a href='/getStateData'> State Data</a> </ui><ui> <a href='/districtpdfurl'>District Pdf Data</a> </ui><ui> <a href='/timeSeries'>TimeSeries Data</a> </ui><ui> <a href='/getDistrictData'> District wise Data</a> </ui><ui> <a href='/GlobalTimeSeries'> Global TimeSeries</a> </ui><ui> <a href='/Dateinfo'> Dateinfo</a> </ui><ui> <a href='/abhishek'> Update Data</a> </ui></li>"

@app.route('/getStateData',methods=['GET'])
def stateData():
	return tableData(getUrl(url))


@app.route('/districtpdfurl',methods=['GET'])
def districtpdfurl():
	return District(getUrl(url))


@app.route('/timeSeries',methods=['GET'])
def TimeSeries():
	return retTimeSeries()


@app.route('/getDistrictData',methods=['GET'])
def DistrictData():
	return retDistrictData();



@app.route('/GlobalTimeSeries',methods=['GET'])
def GlobalTimeSeries():
	return retGlobalTimeSeriesData()



@app.route('/abhishek',methods=['GET'])
def Update_data():
	Write()
	return "success"


@app.route('/Dateinfo',methods=['GET'])
def Dateinfo():
	return retDateinfo()
