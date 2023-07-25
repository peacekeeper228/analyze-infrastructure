from flask import Flask
from flask import render_template, request
import requests
from utils import *
import json
import h3
from BuildDataClasses import *
app = Flask(__name__)

#тестовая
@app.route('/main_page')
def hello_world():
    return render_template('main_page.html', user="test")

@app.route('/')
def basic_page():
    return render_template('main_page.html')

@app.route('/about')
def about():
    return render_template('about_page.html')

@app.route('/statistics')
def statisticsPage():
    r = requests.get("http://connector:8000/counties")
    datacounties = json.loads(r.text)
    if len(datacounties) == 0:
        return "<h1>NO counts</h1>"
    keyscounts = Dictionary.translateListRus(list(datacounties[0].keys()))
    r = requests.get("http://connector:8000/districts")
    datadistricts = json.loads(r.text)
    if len(datadistricts) == 0:
        return "<h1>NO districts</h1>"
    keysdistricts = Dictionary.translateListRus(list(datadistricts[0].keys()))
    return render_template('statistics.html',
                        keyscounts = keyscounts,
                        counts=datacounties,
                        keysdistricts=keysdistricts,
                        datadistricts=datadistricts)

@app.route('/map')
def map_page():
    r = requests.get("http://connector:8000/districtcountyname")
    datadistricts = json.loads(r.text)
    return render_template('map.html', datadistricts=datadistricts)

def makegeojson(data, listThrow = notUsedTypes):
    geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry" : d['geometry'],
            "properties" : Dictionary.translateDictKeysRusThrows(d, listThrow),
        } for d in data]
    }
    return geojson

@app.route('/buildingfullinfo', methods=['POST'])
def buildingfullinfo():
    input_json = request.get_json(force=True)
    database = input_json['database']   
    r = requests.post("http://connector:8000/buildingfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    if database == 0:
        throwList = ['eoid', 'geometry', 'idspatial', 'shortname', 'totalarea', 'nametype', 'storey']
        return makegeojson(data=datadistricts, listThrow=throwList)
    elif database == 3:
        throwList = ['eoid', 'geometry', 'idspatial', 'shortname', 'totalarea', 'nametype', 'storey', 'currentworkload']
        return makegeojson(data=datadistricts, listThrow=throwList)
    elif database == 1:
        throwList = ['eoid', 'geometry', 'idspatial', 'totalarea', 'medtype', 'storey', 'area', 'website']
        return makegeojson(data=datadistricts, listThrow=throwList)
    else:
        return makegeojson(data=datadistricts)

@app.route('/districtsfullinfo', methods=['POST'])
def districtsfullinfo():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/districtsfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    return makegeojson(data=datadistricts)

@app.route('/nearcoordinates', methods=['POST'])
def nearcoordinates():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/pointInDistrict", json=input_json)
    datadistrict = json.loads(r.text)
    districtID = datadistrict[0]["idSpatial"]

    distance = Ravailability(districtID, input_json['database'])
    input_json["distance"] = distance
    input_json["database"] = 2
    r = requests.post("http://connector:8000/nearcoordinatesfullinfo", json=input_json)
    if r.text == '[]':
        return '[]' 
    datadistricts = json.loads(r.text)
    #return datadistricts
    return {"data":makegeojson(data=datadistricts), "radius": distance}

def Ravailability(districtID, buildsType):
    if districtID in centralDistricts:
        if buildsType == 0:
            distance = 750
        elif buildsType == 1:
            distance = 1500
        elif buildsType == 3:
            distance = 500
        else:
            distance = 500
    else:
        if buildsType == 0:
            distance = 500
        elif buildsType == 1:
            distance = 1500
        elif buildsType == 3:
            distance = 300
        else:
            distance = 500
    return distance

@app.route('/hexForDistricts', methods=['POST'])
def hexForDistricts():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/districtsfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    geojson = makegeojson(data=datadistricts)
    return assembleHexagones(geojson, hexagone_size=input_json['hexagone_size'])

def assembleHexagones(data, hexagone_size):
    polylines_list = []
    for i in range(len(data['features'])):
        polylinet = createHexagons(data['features'][i], hexagone_size)
        polylines_list.extend(polylinet)
    return polylines_list

def createHexagons(data, hexagone_size):
        sub_geoJson = data['geometry']
        hexagons = []
        if sub_geoJson['type'] == 'Polygon':
            hexagons = list(h3.polyfill(sub_geoJson, hexagone_size))
        else:
            for i in sub_geoJson['coordinates']:
                sub_sub = {"type": "Polygon", "coordinates": i}
                hexagons.extend(list(h3.polyfill(sub_sub, hexagone_size)))
        return hexagons
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

def change_schools_workload(dist_school_number, dist_school_load, old_number, old_capacity, new_number, new_capacity):
    total_workload = dist_school_number * dist_school_load
    school_old_workload = (old_number / old_capacity * 100)
    without_one_school_workload = total_workload - school_old_workload
    school_new_workload = ((old_number + new_number) / (old_capacity +new_capacity) * 100)
    total_workload = (without_one_school_workload + school_new_workload) / dist_school_number
    return total_workload

def get_provision_flag_school(districi_id, min_ob_index):
    if districi_id in zone_1:
        if min_ob_index >= school_zone_1:
            is_min_ob = 1
        else:
            is_min_ob = 0
    elif districi_id in zone_2:
        if min_ob_index >= school_zone_2:
            is_min_ob = 1
        else:
            is_min_ob = 0
    elif districi_id in zone_3:
        if min_ob_index >= school_zone_3:
            is_min_ob = 1
        else:
            is_min_ob = 0
    return is_min_ob == 1

def get_provision_flag_kindergarten(districi_id, min_ob_index):
    if districi_id in zone_1:
        if min_ob_index >= kinder_zone_1:
            is_min_ob = 1
        else:
            is_min_ob = 0
    elif districi_id in zone_2:
        if min_ob_index >= kinder_zone_2:
            is_min_ob = 1
        else:
            is_min_ob = 0
    elif districi_id in zone_3:
        if min_ob_index >= kinder_zone_3:
            is_min_ob = 1
        else:
            is_min_ob = 0

    return is_min_ob == 1
    
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
        object_dist['schoolprovision'] = get_provision_flag_school(districts_json[i]['iddistrict'], new_schoolprovisionindex)
        object_dist['kindergartenprovision'] = get_provision_flag_kindergarten(districts_json[i]['iddistrict'], new_kindergartenprovisionindex)
        object_dist['actualprovisionindicator'] = new_P
        dist_list.append(object_dist)

    return dist_list

def requestBuildingsFullInfo(database, arrayID):
    postJson = {
        "database": database,
        "arrayID" : arrayID
    }
    try:
        jsonData = requests.post(docker_net + "buildingIDcounty", json=postJson).json()
    except:
        jsonData = []
    return jsonData

@app.route('/checkchanges', methods=['POST'])
def changes():
    input_json_all = request.get_json(force=True)
        
    living = LivingBuildings()
    schools = SchoolBuildings()
    kindergartens = KindergartenBuildings()
    
    for i in input_json_all['data']:
        if living.checkAndInsert(i):
            continue
        if schools.checkAndInsert(i):
            continue
        if kindergartens.checkAndInsert(i):
            continue
        raise ValueError("type of building is undefined " + i['type'])
     
    livingObjects = requestBuildingsFullInfo(living.getDatabaseNumber(), living.getIDList())
    schoolsObjects = requestBuildingsFullInfo(schools.getDatabaseNumber(), schools.getIDList())
    kindergartensObjects = requestBuildingsFullInfo(kindergartens.getDatabaseNumber(), kindergartens.getIDList())
    
    if input_json_all['isCounty']:
        districts = infoAboutSelectedCounties(input_json_all['counties'])    
    else:
        districts = infoAboutSelectedDistricts(input_json_all['districts'])
    
    for i in livingObjects:
        if not districts.checkInDistricts(i['iddistrict']):
            continue
        buildChanges = living.getDataByID(i['buildid'])
        districts.insertChanges(i['iddistrict'], buildChanges, i)

    for i in schoolsObjects:
        if not districts.checkInDistricts(i['iddistrict']):
            continue
        buildChanges = schools.getDataByID(i['buildid'])
        districts.insertChanges(i['iddistrict'], buildChanges, i)

    for i in kindergartensObjects:
        if not districts.checkInDistricts(i['iddistrict']):
            continue
        buildChanges = kindergartens.getDataByID(i['buildid'])
        districts.insertChanges(i['iddistrict'], buildChanges, i)

    if input_json_all['isCounty']:
        models=stat_county(districts.getDistricts())   
    else:
        dist_list = change_district_statistic(districts_json=districts.getDistricts())
        models=stat(dist_list)
    return render_template('statistics.html',
                            models=models,
                            valuesdict=valuesdict)

def infoAboutSelectedDistricts(selectedDistricts):
    dist_post_json = {
        "IDsource": selectedDistricts,
    }
    full_selected_districts = requests.post(docker_net + "districtsinfobyname", json=dist_post_json).json()
    return Districts(full_selected_districts)

def infoAboutSelectedCounties(selectedDistricts):
    county_post_json = {'countynames': selectedDistricts}
    full_selected_districts = requests.post(docker_net + "countyinfobynames", json=county_post_json).json()
    for i in range(len(full_selected_districts)):
        full_selected_districts[i]['iddistrict'] = full_selected_districts[i]['idcount']
        del full_selected_districts[i]['idcount']
    return Districts(full_selected_districts)

def stat(dist_list=[]):
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

def stat_county(county_list):
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
    app.run(host='0.0.0.0', debug = True)