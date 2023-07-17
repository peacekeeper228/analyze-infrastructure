from flask import Flask
from flask import render_template, request
import requests
from utils import *
import json
import h3
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
def main_page():
    r = requests.get("http://connector:8000/counties")
    datacounties = json.loads(r.text)
    if len(datacounties) == 0:
        return "<h1>NO counts</h1>"
    keyscounts = [dictfromdatabase.get(x, x) for x in list(datacounties[0].keys())]
    r = requests.get("http://connector:8000/districts")
    datadistricts = json.loads(r.text)
    if len(datadistricts) == 0:
        return "<h1>NO districts</h1>"
    keysdistricts = [dictfromdatabase.get(x, x) for x in list(datadistricts[0].keys())]
    return render_template('statistics.html',
                        keyscounts = keyscounts,
                        counts=datacounties,
                        keysdistricts=keysdistricts,
                        datadistricts=datadistricts)

@app.route('/map')
def map_page():
    r = requests.get("http://connector:8000/districtcountyname")
    datadistricts = json.loads(r.text)
    #return datadistricts
    return render_template('map.html', user="test2", datadistricts=datadistricts)

def without_keys(d, listThrow):
    if listThrow == []:
        return {dictfromdatabase.get(x, x): d[x] for x in d if x not in notUsedTypes}
    else:
        return {dictfromdatabase.get(x, x): d[x] for x in d if x not in listThrow}

def makegeojson(data, listThrow = []):
    geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : d['geometry'],
        "properties" : without_keys(d, listThrow),
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

    if districtID in centralDistricts:
        if input_json['database'] == 0:
            distance = 750
        elif input_json['database'] == 1:
            distance = 1500
        elif input_json['database'] == 3:
            distance = 500
        else:
            distance = 500
    else:
        if input_json['database'] == 0:
            distance = 500
        elif input_json['database'] == 1:
            distance = 1500
        elif input_json['database'] == 3:
            distance = 300
        else:
            distance = 500
    input_json["distance"] = distance
    input_json["database"] = 2
    r = requests.post("http://connector:8000/nearcoordinatesfullinfo", json=input_json)
    if r.text == '[]':
        return '[]' 
    datadistricts = json.loads(r.text)
    #return datadistricts
    return {"data":makegeojson(data=datadistricts), "radius": distance}


def create_hexagons(data, hexagone_size):
        polylines_list = []
        sub_geoJson = data['geometry']
        hexagons = []
        #hexagons = [h3.polyfill(shapely.geometry.mapping(x)) for x in list(shapely.geometry.loads(sub_geoJson), hexagone_size)]
        if sub_geoJson['type'] == 'Polygon':
            hexagons = list(h3.polyfill(sub_geoJson, hexagone_size))
        else:
            for i in sub_geoJson['coordinates']:
                sub_sub = {"type": "Polygon", "coordinates": i}
                hexagons.extend(list(h3.polyfill(sub_sub, hexagone_size)))

        polylines = []
        for hex in hexagons:
            polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
            outlines = [loop for polygon in polygons for loop in polygon]
            polyline = [outline + [outline[0]] for outline in outlines][0]
            polylines.append(polyline)

            polylines_list.append(polylines)
        
        return hexagons

#Функция для отрисовки гексагонов на карте в пределах выбранных районов
def print_hexagones(data, hexagone_size):
    polylines_list = []
    #maps, polygons_hex, polylines = self.create_hexagons(maps, df_target_borders.iloc[0]['geometry'])
    for i in range(len(data['features'])):
        polylinet = create_hexagons(data['features'][i],
                                    hexagone_size=hexagone_size)
        polylines_list.extend(polylinet)
    return polylines_list

    #print('list_ken', len(self.big_polygons_hex_list_regions), len(self.big_polygons_hex_list_district))


@app.route('/hexForDistricts', methods=['POST'])
def hexForDistricts():
    input_json = request.get_json(force=True)
    r = requests.post("http://connector:8000/districtsfullinfo", json=input_json)
    datadistricts = json.loads(r.text)
    geojson = makegeojson(data=datadistricts)
    return print_hexagones(geojson, hexagone_size=input_json['hexagone_size'])

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
    for i in districts_json:
        object_dist = districts_json[i]['dist']
        old_district_school_capacity = object_dist['schoolprovisionindex'] * object_dist['residentsnumber'] / 1000
        old_district_kinder_capacity = object_dist['kindergartenprovisionindex'] * object_dist['residentsnumber'] / 1000
        old_P = object_dist['actualprovisionindicator']
        old_N = object_dist['residentsnumber']
        old_Q = object_dist['schoolprovisionindex']
        old_D = old_P - (old_N * old_Q) / 1000
        new_district_school_capacity = old_district_school_capacity + districts_json[i].get('school_delta', 0)
        new_district_kinder_capacity = old_district_kinder_capacity + districts_json[i].get('kinder_delta', 0)
        object_dist['residentsnumber'] = object_dist['residentsnumber'] + districts_json[i].get('residents_delta', 0)
        new_schoolprovisionindex = new_district_school_capacity / object_dist['residentsnumber'] * 1000
        new_kindergartenprovisionindex = new_district_kinder_capacity / object_dist['residentsnumber'] * 1000
        new_N = object_dist['residentsnumber']
        new_D = old_D + districts_json[i].get('students_delta', 0) - districts_json[i].get('school_delta', 0)
        new_Q = int(new_schoolprovisionindex)
        new_P = (new_N * new_Q) / 1000 + new_D
        object_dist['schoolprovisionindex'] = new_schoolprovisionindex
        object_dist['kindergartenprovisionindex'] = new_kindergartenprovisionindex
        object_dist['schoolprovision'] = get_provision_flag_school(i, new_schoolprovisionindex)
        object_dist['kindergartenprovision'] = get_provision_flag_kindergarten(i, new_kindergartenprovisionindex)
        object_dist['actualprovisionindicator'] = new_P
        dist_list.append(object_dist)

    return dist_list

#Преобразование данных по районам и округам в папке additional_code ноутбук preparation_for_statistic
@app.route('/stat', methods=['POST', 'GET'])
def stat(dist_list=[], sort_type=''):
    models = {}
    map_for_sorting = {}
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

@app.route('/checkchanges', methods=['POST'])
def changes():
    input_json_all = request.get_json(force=True)
    input_json = input_json_all['data']
    selected_districts = input_json_all['districts']

    schools_list_id = []
    schools_json = []
    buildings_list_id = []
    buildings_json = []
    kinder_list_id = []
    kinder_json = []
    for i in input_json:
        if i['type'] == 'Школа':
            schools_list_id.append(i['id'])
            schools_json.append(i)
        elif i['type'] == 'Жилое':
            buildings_list_id.append(i['id'])
            buildings_json.append(i)
        elif i['type'] == 'Детский сад':
            kinder_list_id.append(i['id'])
            kinder_json.append(i)
    schools_post_json = {
    "database": 0,
    "arrayID" : schools_list_id
    }
    districts_dict = {}
    #Обрабатываем все школы
    schools_object = requests.post(docker_net + "buildingID", json=schools_post_json).json()
    for i in range(len(schools_object)):
        object_dist_id = schools_object[i]['iddistrict']
        if object_dist_id in districts_dict:
            object_dist = districts_dict[object_dist_id]['dist']
            school_total_capacity_delta = districts_dict[object_dist_id]['school_delta']
            school_total_students_delta = districts_dict[object_dist_id]['students_delta']
        else:
            post_json_dist = {'IDsource': [object_dist_id]}
            object_dist = requests.post(docker_net + "districtsID", json=post_json_dist).json()[0]
            school_total_capacity_delta = 0
            school_total_students_delta = 0
            districts_dict[object_dist_id] = {}

        object_dist['schoolload'] = change_schools_workload(object_dist['schoolnumber'], object_dist['schoolload'],
                                schools_object[i]['currentworkload'], schools_object[i]['calculatedworkload'],
                                schools_json[i].get("Количество учеников", 0), schools_json[i].get("Номинальная вместимость", 0))
        school_total_capacity_delta += schools_json[i].get("Номинальная вместимость", 0)
        school_total_students_delta += schools_json[i].get("Количество учеников", 0)


        districts_dict[object_dist_id]['dist'] = object_dist
        districts_dict[object_dist_id]['school_delta'] = school_total_capacity_delta

    #Обрабатываем все детские сады
    kinder_post_json = {
            "database": 3,
            "arrayID": kinder_list_id
        }
    kinder_object = requests.post(docker_net + "buildingID", json=kinder_post_json).json()
    for i in range(len(kinder_object)):
        object_dist_id = kinder_object[i]['iddistrict']
        if object_dist_id in districts_dict:
            object_dist = districts_dict[object_dist_id]['dist']
            kinder_total_capacity_delta = districts_dict[object_dist_id].get('kinder_delta', 0)
        else:
            post_json_dist = {'IDsource': [object_dist_id]}
            object_dist = requests.post(docker_net + "districtsID", json=post_json_dist).json()[0]
            kinder_total_capacity_delta = 0
            districts_dict[object_dist_id] = {}

        kinder_total_capacity_delta += kinder_json[i].get("Номинальная вместимость", 0)
        districts_dict[object_dist_id]['dist'] = object_dist
        districts_dict[object_dist_id]['kinder_delta'] = kinder_total_capacity_delta

    #Обрабатываем все жилые здания
    building_post_json = {
            "database": 2,
            "arrayID": buildings_list_id
        }
    building_object = requests.post(docker_net + "buildingID", json=building_post_json).json()
    for i in range(len(building_object)):
        object_dist_id = building_object[i]['iddistrict']
        if object_dist_id in districts_dict:
            object_dist = districts_dict[object_dist_id]['dist']
            residents_total_capacity_delta = districts_dict[object_dist_id].get('residents_delta', 0)
        else:
            post_json_dist = {'IDsource': [object_dist_id]}
            object_dist = requests.post(docker_net + "districtsID", json=post_json_dist).json()[0]
            districts_dict[object_dist_id] = {}
            residents_total_capacity_delta = 0

        building_object[i]['freeschools'] += buildings_json[i].get('Количество свободных школ', 0)
        residents_total_capacity_delta += buildings_json[i].get("Количество взрослых", 0)
        districts_dict[object_dist_id]['dist'] = object_dist
        districts_dict[object_dist_id]['residents_delta'] = residents_total_capacity_delta

    dist_list = change_district_statistic(districts_dict)

    dist_post_json = {
    "IDsource": selected_districts,
    }
    full_selected_districts = requests.post(docker_net+"districtsinfobyname", json=dist_post_json).json()

    final_dist_list = full_selected_districts.copy()
    for i in dist_list:
        name = i['namedistrict']
        for j in range(len(final_dist_list)):
            if name == final_dist_list[j]['namedistrict']:
                final_dist_list[j] = i

    models = stat(final_dist_list)
    return render_template('statistics.html',
                            models=models,
                            valuesdict=valuesdict)


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
    return models

@app.route('/checkchanges_county', methods=['POST'])
def changes_county():
    input_json_all = request.get_json(force=True)
    input_json = input_json_all['data']
    selected_districts = input_json_all['counties']

    schools_list_id = []
    schools_json = []
    buildings_list_id = []
    buildings_json = []
    kinder_list_id = []
    kinder_json = []
    for i in input_json:
        if i['type'] == 'Школа':
            schools_list_id.append(i['id'])
            schools_json.append(i)
        elif i['type'] == 'Жилое':
            buildings_list_id.append(i['id'])
            buildings_json.append(i)
        elif i['type'] == 'Детский сад':
            kinder_list_id.append(i['id'])
            kinder_json.append(i)
    schools_post_json = {
        "database": 0,
        "arrayID" : schools_list_id
    }
    county_dict = {}
    #Обрабатываем все школы
    schools_object = requests.post(docker_net + "buildingID", json=schools_post_json).json()
    for i in range(len(schools_object)):
        object_dist_id = schools_object[i]['iddistrict']
        county_post_json = {'districtID': object_dist_id}
        county = requests.post(docker_net + "countybydistrict", json=county_post_json).json()[0]
        county_name = county['namecounty']
        if county_name in county_dict:
            object_dist = county_dict[county_name]['dist']
        else:
            object_dist = county
            county_dict[county_name] = {}

        object_dist['schoolload'] = change_schools_workload(object_dist['schoolnumber'], object_dist['schoolload'],
                                schools_object[i]['currentworkload'], schools_object[i]['calculatedworkload'],
                                schools_json[i].get("Количество учеников", 0), schools_json[i].get("Номинальная вместимость", 0))

        county_dict[county_name]['dist'] = object_dist

    #Обрабатываем все жилые здания
    building_post_json = {
            "database": 2,
            "arrayID": buildings_list_id
        }
    building_object = requests.post(docker_net + "buildingID", json=building_post_json).json()
    for i in range(len(building_object)):
        object_dist_id = building_object[i]['iddistrict']
        county_post_json = {'districtID': object_dist_id}
        county = requests.post(docker_net + "countybydistrict", json=county_post_json).json()[0]
        county_name = county['namecounty']
        if county_name in county_dict:
            object_dist = county_dict[county_name]['dist']
        else:
            object_dist = county
            county_dict[county_name] = {}

        object_dist['residentsnumber'] += buildings_json[i].get("Количество взрослых", 0)
        county_dict[county_name]['dist'] = object_dist

    county_list = []
    for i in county_dict:
        county_list.append(county_dict[i]['dist'])

    county_post_json = {'countynames': selected_districts}
    full_selected_county = requests.post(docker_net + "countyinfobynames", json=county_post_json).json()


    final_county_list = full_selected_county.copy()
    for i in county_list:
        name = i['namecounty']
        for j in range(len(final_county_list)):
            if name == final_county_list[j]['namecounty']:
                final_county_list[j] = i

    models = stat_county(final_county_list)

    return render_template('statistics.html',
            models=models,
            valuesdict=valuescounty)

if __name__ == '__main__':
    app.run(host='0.0.0.0')