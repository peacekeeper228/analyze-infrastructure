from flask import Flask
from flask import render_template, request
import requests
from utils import *
import json
from Buildings import *
from models import *

from formula import *
from workingWithHexagones import *
import os, sys
from changingStatistics import changeDistrictStatistic, transformInfoCounties, transformInfoDistricts

app = Flask(__name__)
sys.path.append(os.getcwd())
@app.route('/main_page')
def hello_world():
    return render_template('main_page.html', user="test")

@app.route('/')
def basic_page():
    return render_template('main_page.html')

@app.route('/about')
def about():
    return render_template('about_page.html')

@app.route('/map')
def map_page():
    r = requests.get("http://connector:8000/districtcountyname")
    datadistricts = json.loads(r.text)
    return render_template('map.html', datadistricts=datadistricts)

@app.route('/buildingfullinfo', methods=['POST'])
def buildingfullinfo():
    input_json = request.get_json(force=True)
    database = input_json['database']   
    r = requests.post("http://connector:8000/buildingfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    return makeGeojson(datadistricts, throwListForDatabases[database])

@app.route('/districtsfullinfo', methods=['POST'])
def districtsfullinfo():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/districtsfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    return makeGeojson(data=datadistricts)

@app.route('/nearcoordinates', methods=['POST'])
def nearcoordinates():
    input_json = request.get_json(force=True)
    districtID = getSpatialIDDistrictByCoordinates(input_json['database'], input_json['database'])
    distance = Ravailability(districtID, input_json['database'])
    input_json["distance"] = distance
    input_json["database"] = 2
    r = requests.post("http://connector:8000/nearcoordinatesfullinfo", json=input_json)
    if r.text == '[]':
        return '[]' 
    datadistricts = json.loads(r.text)
    return {"data":makeGeojson(data=datadistricts), "radius": distance}

@app.route('/hexForDistricts', methods=['POST'])
def hexForDistricts():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/districtsfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    geojson = makeGeojson(data=datadistricts)
    return assembleHexagones(geojson, hexagone_size=input_json['hexagone_size'])

'''
{
    "IDsource": ["район Ивановское", "Бабушкинский район"],
  	"hexagone_size": 9
}
'''

@app.route('/checkforschool', methods=['POST'])
def checkforschool():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/changesforschool", json=input_json)
    dataAboutSchools = json.loads(r.text)
    return dataAboutSchools
    
@app.route('/checkchanges', methods=['POST'])
def changes():
    input_json_all = request.get_json(force=True)
    Buildings = BuildingsCollection() 
    
    for i in input_json_all['data']:
        Buildings.insertDataAccordingToType(i)

    for i in range(len(Buildings.buildingCollection)):
        Buildings.buildingCollection[i].setObjects(requestBuildingsFullInfo(
            Buildings.buildingCollection[i].getDatabaseNumber(),
            Buildings.buildingCollection[i].getIDList()))
    if input_json_all['isCounty']:
        municipalities = infoAboutSelectedCounties(input_json_all['counties'])    
    else:
        municipalities = infoAboutSelectedDistricts(input_json_all['districts'])
    
    for objectCollection in Buildings.buildingCollection:
        for i in objectCollection.getObjects():
            if input_json_all['isCounty']:
                municipalityID = i['idcount']
            else:
                municipalityID = i['iddistrict']
            if not municipalities.checkInMunicipalities(municipalityID):
                continue
            buildChanges = objectCollection.getDataByID(i['buildid'])
            municipalities.insertChanges(municipalityID, buildChanges, i)
    if input_json_all['isCounty']:
        models=transformInfoCounties(municipalities.getMunicipalities())   
    else:
        dist_list = changeDistrictStatistic(districts_json=municipalities.getMunicipalities())
        models=transformInfoDistricts(dist_list)

    return render_template('statistics.html',
                            models=models,
                            valuesdict=valuesdict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
