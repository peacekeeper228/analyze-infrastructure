
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from toPostgresDB import *
from toMongoDB import *

app = FastAPI()

dictDatabases = {
    0: 'eduBuildings', #Школы
    1: 'medBuildings',
    2: 'livingBuildings',
    3: 'eduBuildings' #Детские сады
}
dictfields = {
    0: 'schoolnumber', #Школы
    1: 'medicineNumber',
    2: 'livingNumber',
    3: 'kindergartenNumber' #Детские сады
}

def makeArrayIDspatial(data):
    return [i['idspatial'] for i in data]

def schooltype():
    return " and t.nameType = 'Школа' "

def kindergartentype():
    return " and t.nameType = 'Детский сад' "

@app.get("/counties")
async def counties():
    dataBaseLink = dbPostgresGetCounties()
    return JSONResponse(content=dataBaseLink.query(), status_code=200)

@app.get("/countiesname")
async def countiesname():
    dataBaseLink = dbPostgresGetCounties()
    return [x['namecounty'] for x in dataBaseLink.query()]

@app.get("/districts")
async def districts():
    dataBaseLink = dbPostgresGetDistricts()
    return dataBaseLink.query()

@app.post("/districts")
async def districts(request: Request):
    dataBaseLink = dbPostgresGetDistrictsWithCounyNameByID()
    jsonbody = await request.json()
    return dataBaseLink.query(jsonbody['arrayID'])
'''
{
 	"arrayID": [1,2] 
}
'''

@app.get("/districtsname")
async def districtsname():
    dataBaseLink = dbPostgresGetDistricts()
    return {x['namedistrict']:x['namedistrict'] for x in dataBaseLink.query()}

@app.get("/districtcountyname")
async def districtcountyname():
    dataBaseLink = dbPostgresGetDistricts()
    result = {}
    for i in dataBaseLink.query():
        if i['namecounty'] not in result.keys():
            result[i['namecounty']] = [i['namedistrict']]
        else:
            result[i['namecounty']].append(i['namedistrict'])
    return result

@app.post("/buildingin")
async def schoolsin(request: Request):
    jsonbody = await request.json()
    selecttype = ''
    if jsonbody['database'] == 0:
        selecttype = schooltype()
    elif jsonbody['database'] == 3:
        selecttype = kindergartentype()
    database = dictDatabases[jsonbody['database']]
    if jsonbody['isCounty']:
        dataBaseLink = dbPostgresGetInCounty()
        return JSONResponse(content=dataBaseLink.query(jsonbody['IDsource'], database, selecttype), status_code=200)
    else:
        dataBaseLink = dbPostgresGetInDistrict()
        return JSONResponse(content=dataBaseLink.query(jsonbody['IDsource'], database, selecttype), status_code=200)
'''
{
    "IDsource": "relation/1299013",
  	"isCounty": false,
  	"database": 1
}
'''
@app.post("/buildingID")
async def schoolsin(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    if jsonbody['arrayID'] == []:
        return []
    t = dbPostgresGetByID()
    return JSONResponse(content=t.query(jsonbody['arrayID'], database), status_code=200)
'''
{
    "database": 1,
    "arrayID" : [1,2,3]
}
'''

@app.post("/buildingfullinfo")
async def schoolsfull(request: Request):
    jsonbody = await request.json()
    selecttype = ''
    if jsonbody['database'] == 0:
        selecttype = schooltype()
    elif jsonbody['database'] == 3:
        selecttype = kindergartentype()
    database = dictDatabases[jsonbody['database']]
    if jsonbody['isCounty']:
        t = dbPostgresGetInCounty()
        table = t.query(jsonbody['IDsource'], database, selecttype)
    else:
        t = dbPostgresGetInDistrict()
        table = t.query(jsonbody['IDsource'], database, selecttype)
    listID = makeArrayIDspatial(table)
    mongoLink = dbMongoGetCentroidAndDAtaByID()
    tableMongo = mongoLink.query(listID, database)
    result = []
    for p, m in zip(table, tableMongo):
        res = dict(p, **m)
        result.append(res)
    
    return JSONResponse(content=result, status_code=200)
'''
{
    "IDsource": ["район Ивановское"],
  	"isCounty": false,
  	"database": 1
}
'''
@app.post("/districtsID")
async def schoolsfull(request: Request):
    jsonbody = await request.json()
    t = dbPostgresGetDistrictsByID()
    table = t.query(jsonbody['IDsource'])
    return JSONResponse(content=table, status_code=200)

@app.post("/districtsfullinfo")
async def schoolsfull(request: Request):
    jsonbody = await request.json()
    linkToPostgres = dbPostgresGetDistrictsByName()
    table = linkToPostgres.query(jsonbody['IDsource'])
    listID = makeArrayIDspatial(table)
    mongoLink = dbMongoGetCentroidAndDAtaByID()
    tableMongo = mongoLink.query(listID, 'districts')
    result = []
    for p, m in zip(table, tableMongo):
        res = dict(p, **m)
        result.append(res)
    return JSONResponse(content=result, status_code=200)

@app.post("/mongolist")
async def mongolist(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    listID = jsonbody['listID']
    mongoLink = dbMongoGetCentroidAndDAtaByID()
    return JSONResponse(content=mongoLink.query(listID, database), status_code=200)
'''
{
	"database": 0,
	"listID": [1, 2]
}
'''

@app.get("/mongocollections")
async def mongocollections():
    mongoLink = dbMongoGetAllCollections()
    return JSONResponse(content=mongoLink.query(), status_code=200)

@app.post("/incoordinates")
async def incoordinates(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    Slat = jsonbody['Slat']
    Nlat = jsonbody['Nlat']
    Wlon = jsonbody['Wlon']
    Elon = jsonbody['Elon']
    poly = { "type" : "Polygon", "coordinates" : [[
        [Elon, Slat],
        [Elon, Nlat],
        [Wlon, Nlat],
        [Wlon, Slat],
        [Elon, Slat]]]}
    mongoLink = dbMongoGetWithinCoordinates()
    return JSONResponse(content=mongoLink.query(poly, database), status_code=200)


@app.post("/pointInDistrict")
async def incoordinates(request: Request):
    jsonbody = await request.json()
    database = "districts"
    lat = jsonbody['lat']
    lon = jsonbody['lon']
    poly = { "type" : "Point", "coordinates" : 
        [lon, lat] }
    mongoLink = dbMongoGetWithinCoordinates()
    return JSONResponse(content=mongoLink.query(poly, database), status_code=200)
'''
{
    "lon": 37.93,
    "lat": 55.69
}

{
    "type": "Point",
    "coordinates": [37.938057458250945, 55.70359857748261]
}
'''

@app.post("/nearcoordinates")
async def nearcoordinates(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    lat = jsonbody['lat']
    lon = jsonbody['lon']
    distance = jsonbody['distance']
    poly = { "type" : "Point", "coordinates" : [lon, lat] }
    mongoLink = dbMongoGetNearCoordinates()
    return JSONResponse(content=mongoLink.query(poly, distance, database), status_code=200)
'''
{
    "lon": 37.93,
    "lat": 55.7,
 	"distance": 100,
    "database": 1
}
'''
@app.post("/nearcoordinatesdistance")
async def nearcoordinatesdistance(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    lat = jsonbody['lat']
    lon = jsonbody['lon']
    distance = jsonbody.get('distance', 1000)
    poly = { "type" : "Point", "coordinates" : [lon, lat] }
    mongoLink = dbMongoGetNearCoordinatesWithDistance()
    return JSONResponse(content=mongoLink.query(poly, distance, database), status_code=200)
'''
{
    "lon": 37.93,
    "lat": 55.7,
 	"distance": 1000,
    "database": 2
}
distance is optional and equal to 1000 m dy default
'''

@app.post("/nearcoordinatesfullinfo")
async def nearcoordinates(request: Request):
    jsonbody = await request.json()
    database = dictDatabases[jsonbody['database']]
    lat = jsonbody['lat']
    lon = jsonbody['lon']
    distance = jsonbody['distance']
    poly = { "type" : "Point", "coordinates" : [lon, lat] }
    mongoLink = dbMongoGetNearCoordinates()
    spatialInfo = mongoLink.query(poly, distance, database)
    arrayID = [i['idSpatial'] for i in spatialInfo]
    db = dbPostgresGetBySpatialID()
    table = db.query(arrayID, database)
    result = []
    for p, m in zip(table, spatialInfo):
        res = dict(p, **m)
        result.append(res)
    return JSONResponse(content=result, status_code=200)

@app.post("/changesforschool")
async def changesforschool(request: Request):
    databaseSchool = dictDatabases[0]
    databaseLiving = dictDatabases[2]

    jsonbody = await request.json()
    arraySchoolID = jsonbody.keys()
    t1 = dbPostgresGetByID()
    table = t1.query(arraySchoolID, databaseSchool)
    dictData = {}
    for i in table:
        value = (-1, 1)[jsonbody[str(i['buildid'])]]
        data = str(i['idspatial'])
        dictData[data] = value
    mongoLink = dbMongoGetCentroidAndDAtaByID()
    array1 = [int(a) for a, _ in dictData.items()]
    tableMongo = mongoLink.query(array1, databaseSchool)
    
    listOfContent = []
    for i in tableMongo:
        poly = { "type" : "Point", "coordinates" : [i['longitude'], i['latitude']] }
        mongoLink = dbMongoGetNearCoordinates()
        distance = rAvailabilityForSchool(poly)
        spatialInfo = mongoLink.query(poly, distance, databaseLiving)
        for j in spatialInfo:
            flag = True
            for z in range(len(listOfContent)):
                if j['idSpatial'] == listOfContent[z]['idSpatial']:
                    listOfContent[z]['freeschools'] += dictData[str(i['idSpatial'])]
                    flag = False
                    break
            if flag:
                listOfContent.append({'idSpatial':j['idSpatial'], "freeschools": dictData[str(i['idSpatial'])]})
    arrayIDbuildings = [i['idSpatial'] for i in listOfContent]
    fullDataAboutBuildings = t1.getBySpatialID(arrayIDbuildings, databaseLiving)
    reslist = []
    for item in listOfContent:
        if item['freeschools'] != 0:
            for j in fullDataAboutBuildings:
                if item['idSpatial'] == j['idspatial']:
                    resdict = {
                        'service':
                        {'objectid': j['buildid'],
                         'type': 'Жилое'},
                        'data':{
                        'Количество свободных школ': item['freeschools']},
                        'olddata':{
                        'Количество свободных школ': j['freeschools']},
                    }
                    reslist.append(resdict)
                    break
    return reslist

def rAvailabilityForSchool(polygon):
    mongoLink = dbMongoGetWithinCoordinates()
    datadistrict = mongoLink.query(polygon, "districts")
    districtID = datadistrict[0]["idSpatial"]
    if districtID in centralDistricts:
        return 750
    else:
        return 500

centralDistricts = [
    105,
    13,
    103,
    106,
    108,
    102,
    9,
    107,
    51,
    104
]
@app.post("/districtsinfobyname")
async def schoolsfull(request: Request):
    jsonbody = await request.json()
    t = dbPostgresGetDistrictsByName()
    table = t.query(jsonbody['IDsource'])
    return table 

@app.post("/countyinfobynames")
async def schoolsfull(request: Request):
    jsonbody = await request.json()
    t = dbPostgresGetCountiesByName()
    table = t.query(jsonbody['countynames'])
    return table 

@app.post("/countybydistrict")
async def districts(request: Request):
    t = dbPostgresGetCountybyIDdistrict()
    jsonbody = await request.json()
    return t.query(jsonbody['districtID'])

@app.post("/countybydistrictname")
async def districts(request: Request):
    t = dbPostgresGetCountybyDistrictName()
    jsonbody = await request.json()
    return t.query(jsonbody['districtName'])