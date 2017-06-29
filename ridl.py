from flask import Flask
from flask_ask import request,Ask,statement,question,session
import requests
import pdb


places = {'long beach':"33.77,-118.19","chantilly":"38.8942,77.4311"}

app = Flask(__name__) 

ask = Ask(app,"/")
global has_map
def request_string(text):
	http_string = "http://localhost:8000/text/"
	request_string=http_string + text
	return request_string	

@ask.intent("yesintent")
def yes():
	return statement("Great let's get started")

@ask.intent('introduction')
def intro():
	speech_text ="I am R.I.D.L.  I am here to help you. My purpose is to\
	reduce your time to insight by retrieving and analyzing any data you request. "
	rs = request_string(speech_text)
	requests.get(rs)	
	return statement(speech_text).simple_card("hello")

@ask.intent('datasets') 
def dataset(): 
	timestamp = request['timestamp']
	speech_text="I have one dataset in my system.  I have marine\
	traffic data also called  A-I-S data for the year 2014.  The data\
	is primarily for the Port of Long Beach.\
	The dataset contains 5366060 ship locations from Feb 1 to March 3"
	rs = request_string(speech_text)
	requests.get(rs)	
	return statement(speech_text).simple_card("datasets")


@ask.intent('mapmaker')
def makemap(city,foo):
	global has_map 	
	#pdb.set_trace()	
	tmp_string = ""	
	speech_text = "Building a map for {0}".format(city)		
	try:
		city_lower = city.lower()
	except:
		city_lower ='foo'
	if city_lower  in places.keys():
		latlon = places[city_lower]
		tmp_string = "http://localhost:8000/map/"+city_lower
	if foo != None and has_map == 1:	
		has_map = 2	
		requests.get("http://localhost:8000/removelast/")
		requests.get("http://localhost:8000/map/33.77,-118.193,x.geojson")
	elif foo!= None and has_map == 0:
		requests.get("http://localhost:8000/map/33.77,-118.193,x.geojson")
	else:	
		has_map = 1
		requests.get("http://localhost:8000/map/33.77,-118.193")
	return statement(speech_text).simple_card("hello")
@ask.intent('genplots')
def plotlyp():
	requests.get("http://localhost:8000/genplot")
	return statement("Returning registry information") 
	
@ask.intent('plotships')
def plotships(dates,datee):
	speech_text = "Plotting ships on the map"	
	requests.get("http://localhost:8000/plotships/")
	rs = request_string(speech_text)
	return statement(speech_text)

if __name__ == '__main__':
	global has_map 	
	has_map =0 	
	app.run(port=5000,debug=True)
