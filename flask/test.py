from BuildDataClasses import *

input_json_all = {'data': [{'Номинальная вместимость': 3402000, 'Загруженность (в процентах от номинальной)': 16.3829787234042, 'id': 1, 'type': 'Школа'}, {'Количество взрослых': 135900000000, 'id': 24732, 'type': 'Жилое'}, {'Номинальная вместимость': 936000, 'id': 2865, 'type': 'Детский сад'}],
                       'districts': ['район Богородское', 'район Вешняки', 'район Восточное Измайлово', 'район Гольяново', 'район Ивановское', 'район Измайлово', 'район Косино-Ухтомский', 'район Метрогородок', 'район Новогиреево', 'район Новокосино', 'район Перово', 'район Преображенское', 'район Северное Измайлово', 'район Соколиная Гора', 'район Сокольники']}
    #                  'districts': ['Восточный административный округ']}

living = LivingBuildings()
schools = SchoolBuildings()
kindergartens = KindergartenBuildings()

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
        new_D = old_D + districts_json[i].get('schoolTotalStudentsDelta', 0)
        new_Q = int(new_schoolprovisionindex)
        new_P = (new_N * new_Q) / 1000 + new_D
        object_dist['schoolprovisionindex'] = new_schoolprovisionindex
        object_dist['kindergartenprovisionindex'] = new_kindergartenprovisionindex
        object_dist['schoolprovision'] = get_provision_flag_school(i, new_schoolprovisionindex)
        object_dist['kindergartenprovision'] = get_provision_flag_kindergarten(i, new_kindergartenprovisionindex)
        object_dist['actualprovisionindicator'] = new_P
        dist_list.append(object_dist)

    return dist_list

def get_provision_flag_school(a, b):
    return 1
def get_provision_flag_kindergarten(a, b):
    return 1

for i in input_json_all['data']:
    if living.checkAndInsert(i):
        continue
    if schools.checkAndInsert(i):
        continue
    if kindergartens.checkAndInsert(i):
        continue
    raise ValueError("type of building is undefined " + i['type'])
    
print(0)

livingObjects = [{
    "buildid": 24732,
    "adress": "9-я Парковая улица 70 к1",
    "flats": 80,
    "area": 4546.2,
    "storey": 5,
    "buildyear": 1961,
    "children": 10,
    "pupils": 25,
    "adults": 1501,
    "freeschools": 0,
    "availableschools": 3,
    "availablekindergartens": 0,
    "availablemedicine": 23,
    "idspatial": 24732,
    "iddistrict": "relation/1319263"
}]
schoolsObjects = [{
    "buildid": 1,
    "fullname": "Государственное бюджетное общеобразовательное учреждение города Москвы «Школа № 2048»",
    "shortname": "ГБОУ школа № 2048",
    "website": "2048.mskobr.ru",
    "adress": "город Москва, улица Липчанского, дом 6А",
    "area": 1307.0,
    "storey": 5,
    "calculatedworkload": 326,
    "currentworkload": 4779,
    "totalarea": 6535.0,
    "idspatial": 1,
    "rating": 0.0,
    "eoid": 12960,
    "iddistrict": "relation/1319142",
    "nametype": "Школа"
}]
kindergartensObjects = [{
    "buildid": 2865,
    "fullname": "Государственное бюджетное общеобразовательное учреждение города Москвы «Школа № 319»",
    "shortname": "ГБОУ школа № 319",
    "website": "sch319v.mskobr.ru",
    "adress": "город Москва, Амурская улица, дом 72",
    "area": 1046.063,
    "storey": 2,
    "calculatedworkload": 104,
    "currentworkload": 0,
    "totalarea": 2092.126,
    "idspatial": 1827,
    "rating": 4.4,
    "eoid": 10141,
    "iddistrict": "relation/1319142",
    "nametype": "Детский сад"
}]

dist_post_json = {
"IDsource": input_json_all['districts'],
}
full_selected_districts = [{
    "iddistrict": "relation/1319142",
    "namedistrict": "район Ивановское",
    "area": 10140564.0,
    "idspatial": 57,
    "schoolnumber": 15,
    "schoolload": 161.86667,
    "kindergartennumber": 27,
    "medicinenumber": 8,
    "livingnumber": 241,
    "residentsnumber": 104474,
    "avgyear": 1975,
    "withoutschools": 8,
    "withoutkindergartens": 31,
    "withoutmedicine": 0,
    "schoolprovisionindex": 55,
    "kindergartenprovisionindex": 38,
    "schoolprovision": False,
    "kindergartenprovision": False,
    "targetprovisionindicator": 15347.088,
    "actualprovisionindicator": 9392.07,
    "density": 0.2514
}]

disricts = Districts(full_selected_districts)

for i in livingObjects:
    if not disricts.checkInDistricts(i['iddistrict']):
        continue
    buildChanges = living.getDataByID(i['buildid'])
    disricts.insertChanges(i['iddistrict'], buildChanges, i)

for i in schoolsObjects:
    if not disricts.checkInDistricts(i['iddistrict']):
        continue
    buildChanges = schools.getDataByID(i['buildid'])
    disricts.insertChanges(i['iddistrict'], buildChanges, i)

for i in kindergartensObjects:
    if not disricts.checkInDistricts(i['iddistrict']):
        continue
    buildChanges = kindergartens.getDataByID(i['buildid'])
    disricts.insertChanges(i['iddistrict'], buildChanges, i)

dist_list = change_district_statistic(districts_json=disricts.getDistricts())
print(0)
