import sys
import os
import pytest
import requests
import requests_mock

sys.path.append( os.path.join( os.path.dirname(__file__), ".." ))
from flask.Municipality import calculateWorkloadInSchool, changeWorkloadInDistrict
from flask.utils import isDisrictProvisionWithSchool, isDistrictProvisionWithKindergarten, Dictionary, Ravailability, schooltype, kindergartentype, makeGeojson

#sys.path.append( os.path.join( os.path.dirname(__file__), "..", "flask", "models" ))

def test_calculatingWorkload():
    assert calculateWorkloadInSchool(100, 100) == 100
    assert calculateWorkloadInSchool(200, 50) == 400

def test_changeWorkloadInDistrict():
    assert changeWorkloadInDistrict(2, 100, 100, 200) == 150
    assert changeWorkloadInDistrict(1, 50, 50, 100) == 100

def test_provisionFlag():
    #zone1
    assert isDisrictProvisionWithSchool('relation/1281220', 200) == True
    assert isDisrictProvisionWithSchool('relation/1250526', 100) == False
    #zone2
    assert isDisrictProvisionWithSchool('relation/1319060', 200) == True
    assert isDisrictProvisionWithSchool('relation/1292286', 100) == False
    #zone3
    assert isDisrictProvisionWithSchool('relation/380702', 200) == True
    assert isDisrictProvisionWithSchool('relation/380703', 100) == False

    with pytest.raises(ValueError):
        isDisrictProvisionWithSchool('notID', 100)

    #zone1
    assert isDistrictProvisionWithKindergarten('relation/1281220', 47) == True
    assert isDistrictProvisionWithKindergarten('relation/1250526', 40) == False
    #zone2
    assert isDistrictProvisionWithKindergarten('relation/1319060', 60) == True
    assert isDistrictProvisionWithKindergarten('relation/1292286', 40) == False
    #zone3
    assert isDistrictProvisionWithKindergarten('relation/380702', 70) == True
    assert isDistrictProvisionWithKindergarten('relation/380703', 40) == False

    with pytest.raises(ValueError):
        isDistrictProvisionWithKindergarten('notID', 100)

def test_Ravailability():
    districtID = 105
    assert Ravailability(districtID, 0) == 750
    assert Ravailability(districtID, 1) == 1500
    assert Ravailability(districtID, 3) == 500

    districtID = 100
    assert Ravailability(districtID, 0) == 500
    assert Ravailability(districtID, 1) == 1500
    assert Ravailability(districtID, 3) == 300

def test_schooltype():
    assert schooltype() == " and t.nameType = 'Школа' "

def test_kindergartentype():
    assert kindergartentype() == " and t.nameType = 'Детский сад' "

    with pytest.raises(ValueError):
        assert Ravailability(100, 10)

def test_dictionary():
    assert Dictionary.getRusNameOrEngDefault("sdfsdk") == "sdfsdk"
    assert Dictionary.getRusNameOrEngDefault("adress") == "Адрес"
    assert Dictionary.translateListRus(["sdfsdk", "adress"]) == ["sdfsdk", "Адрес"]

    values = {"sdfsdk": 12, "adress": 15}
    assert Dictionary.translateDictKeysRusThrows(values) == {"sdfsdk": 12, "Адрес": 15}

    assert Dictionary.translateDictKeysRusThrows(values, ['adress']) == {"sdfsdk": 12}

def test_makeGeojson():
    data = [{
        "geometry": {
            "type": "Point",
            "coordinates": [37.938057458250945, 55.70359857748261]
        },
        "adress": "Город Москва",
        "sdfsdk": 15
    }]
    expected_dict = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry" : {"type": "Point","coordinates": [37.938057458250945, 55.70359857748261]},
            "properties" : {"sdfsdk": 15, "Адрес": "Город Москва"}
        }]
    }
    assert makeGeojson(data) == expected_dict
    expected_dict = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry" : {"type": "Point","coordinates": [37.938057458250945, 55.70359857748261]},
            "properties" : {"Адрес": "Город Москва"}
        }]
    }
    assert makeGeojson(data, ["sdfsdk"]) == expected_dict