from flask import Flask
from flask import render_template, request
import requests
from utils import *
import json
from Buildings import *
from typing import List
from Municipality import Municipalities
from models import *
from workingWithHexagones import *
app = Flask(__name__)

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
    
def change_district_statistic(districts_json):

    dist_list = []
    for i in range(len(districts_json)):
        object_dist = districts_json[i]
        old_district_school_capacity = object_dist['schoolprovisionindex'] * object_dist['residentsnumber'] / 1000
        old_district_kinder_capacity = object_dist['kindergartenprovisionindex'] * object_dist['residentsnumber'] / 1000
        old_P = object_dist['actualprovisionindicator']
        old_N = object_dist['residentsnumber']
        old_Q = object_dist['schoolprovisionindex']
        old_D = old_P - (old_N * old_Q) / 1000
        new_district_school_capacity = old_district_school_capacity + districts_json[i].get('schoolTotalCapacityDelta', 0)
        new_district_kinder_capacity = old_district_kinder_capacity + districts_json[i].get('kinderTotalCapacityDelta', 0)
        object_dist['residentsnumber'] = object_dist['residentsnumber'] + districts_json[i].get('residents_delta', 0)
        new_schoolprovisionindex = new_district_school_capacity / object_dist['residentsnumber'] * 1000
        new_kindergartenprovisionindex = new_district_kinder_capacity / object_dist['residentsnumber'] * 1000
        new_N = object_dist['residentsnumber']
        new_D = old_D + districts_json[i].get('schoolTotalStudentsDelta', 0) - districts_json[i].get('schoolTotalCapacityDelta', 0)
        new_Q = int(new_schoolprovisionindex)
        new_P = (new_N * new_Q) / 1000 + new_D
        object_dist['schoolprovisionindex'] = new_schoolprovisionindex
        object_dist['kindergartenprovisionindex'] = new_kindergartenprovisionindex
        object_dist['schoolprovision'] = isDisrictProvisionWithSchool(districts_json[i]['iddistrict'], new_schoolprovisionindex)
        object_dist['kindergartenprovision'] = isDistrictProvisionWithKindergarten(districts_json[i]['iddistrict'], new_kindergartenprovisionindex)
        object_dist['actualprovisionindicator'] = new_P
        dist_list.append(object_dist)

    return dist_list

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
        dist_list = change_district_statistic(districts_json=municipalities.getMunicipalities())
        models=transformInfoDistricts(dist_list)

    return render_template('statistics.html',
                            models=models,
                            valuesdict=valuesdict)

def transformInfoDistricts(dist_list=[]):
    models = {}
    if len(dist_list) > 0:
        for i in dist_list:
            territories = i['namedistrict']
            is_schools_obespech = ('Нет','Да')[i['schoolprovision']]
            is_kinder_obespech = ('Нет','Да')[i['kindergartenprovision']]

            models[territories] = {'Площадь (м2)': round(i['area'], 0),
                'Количество школ': round(i['schoolnumber'], 0),
                'Средняя загруженность школ(в процентах)': round(i['schoolload'], 0),
                'Количество детских садов': round(i['kindergartennumber'], 0),
                'Количество мед учреждений': round(i['medicinenumber'], 0),
                'Количество жилых домов': round(i['livingnumber'], 0),
                'Количество жителей': round(i['residentsnumber'], 0),
                'Средний год постройки зданий': round(i['avgyear'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от школ': round(i['withoutschools'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от детских садов': round(i['withoutkindergartens'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от медицинских учреждений': round(i['withoutmedicine'], 0),
                'Количество мест в школах (на 1000 человек)': round(i['schoolprovisionindex'], 0),
                'Удовлетворяет ли количество мест в школах нормативам': is_schools_obespech,
                'Количество мест в детских садах (на 1000 человек)': round(i['kindergartenprovisionindex'], 0),
                'Удовлетворяет ли количество мест детских садах нормативам': is_kinder_obespech,
                'Целевой показатель минимально допустимого уровня обеспеченности населения школами': round(i['targetprovisionindicator'], 0),
                'Фактический показатель минимально допустимого уровня обеспеченности населения школами': round(i['actualprovisionindicator'], 0),
                'Плотность жилой застройки': round(i['density'], 4)}
    else:
        models['Список выбранных территорий'] = 'Территории не выбраны'

    return models

def transformInfoCounties(county_list):
    models = {}
    if len(county_list) > 0:
        for i in county_list:
            territories = i['namecounty']
            models[territories] = {'Площадь (м2)': round(i['area'], 0),
                'Количество школ': round(i['schoolnumber'], 0),
                'Средняя загруженность школ(в процентах)': round(i['schoolload'], 0),
                'Количество детских садов': round(i['kindergartennumber'], 0),
                'Количество мед учреждений': round(i['medicinenumber'], 0),
                'Количество жилых домов': round(i['livingnumber'], 0),
                'Количество жителей': round(i['residentsnumber'], 0),
                'Средний год постройки зданий': round(i['avgyear'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от школ': round(i['withoutschools'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от детских садов': round(i['withoutkindergartens'], 0),
                'Процент домов,находящихся вне установленной зоны пешей доступности от медицинских учреждений': round(i['withoutmedicine'], 0)}
    else:
        models['Список выбранных территорий'] = 'Территории не выбраны'
    return models

if __name__ == '__main__':
    app.run(host='0.0.0.0')
