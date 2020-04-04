import flask
import requests
from bs4 import BeautifulSoup
import json
from app.timeSeries import retTimeSeries

url = "https://mohfw.gov.in"


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def tableData(soup):
	data = {}
	response = {}
	table = soup.find('table', class_='table').find('tbody')
	tab_ = table.find_all('tr');
	time = soup.find('div',class_="status-update").find('span')
	response['update-time'] = time.text
	f = open('data/table.html','w')
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

	with open('data/data.json', 'w') as writer:
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
    return "<h1>Distant Reading Archive</h1>Api for Covid Data for India</p> <li><ui> <a href='/getStateData'> State Data</a> </ui><ui> <a href='/districtData'>District Data</a> </ui><ui> <a href='/timeSeries'>TimeSeries Data</a> </ui></li>"

@app.route('/getStateData',methods=['GET'])
def stateData():
	return tableData(getUrl(url))


@app.route('/districtData',methods=['GET'])
def districtData():
	return District(getUrl(url))


@app.route('/timeSeries',methods=['GET'])
def TimeSeries():
	return retTimeSeries()
