import sys
import os
import pytest
import requests
import requests_mock

sys.path.append( os.path.join( os.path.dirname(__file__), ".." ))
from flask.Municipality import Municipalities

municipality1 = {'iddistrict': '10', 'schoolnumber': 2, 'schoolload': 50}
municipality2 = {'iddistrict': '11', 'schoolnumber': 4}
listMunicipalities = [municipality1, municipality2]
municipalities = Municipalities(listMunicipalities)
firstDistrictID = '10'

def test_getMunicipalities():
    assert listMunicipalities == municipalities.getMunicipalities()

def test_checkInMunicipalities():
    assert municipalities.checkInMunicipalities(firstDistrictID) == True
    assert municipalities.checkInMunicipalities('111') == False

def test_getMunicipality():
    assert municipalities.getMunicipality(firstDistrictID) == municipality1
    with pytest.raises(ValueError):
        municipalities.getMunicipality('not a municipality')
    with pytest.raises(ValueError):
        municipalities.getMunicipality(10)

def test_getNumberMunicipality():
    assert municipalities.getNumberMunicipality(firstDistrictID) == 0
    with pytest.raises(ValueError):
        municipalities.getNumberMunicipality('not a municipality')
    with pytest.raises(ValueError):
        municipalities.getNumberMunicipality(10)

def test_getMunicipalitiesID():
    assert municipalities.getMunicipalitiesID() == set([municipality1['iddistrict'], municipality2['iddistrict']])

changedValue = 1000
changedValue2 = 500
def test_insertChangesKindergartens():
    
    dictChanges =  {'Номинальная вместимость': changedValue, 'id': firstDistrictID, 'type': 'Детский сад'}
    municipalities.insertChanges(firstDistrictID, dictChanges)
    assert municipalities.getMunicipality(firstDistrictID)['kinderTotalCapacityDelta'] == changedValue

    dictChanges =  {'Номинальная вместимость': changedValue2, 'id': firstDistrictID, 'type': 'Детский сад'}
    municipalities.insertChanges(firstDistrictID, dictChanges)
    assert municipalities.getMunicipality(firstDistrictID)['kinderTotalCapacityDelta'] == changedValue + changedValue2

def test_insertChangesLiving():
    dictChanges =  {'Количество взрослых': changedValue, 'id': firstDistrictID, 'type': 'Жилое'}
    municipalities.insertChanges(firstDistrictID, dictChanges)
    assert municipalities.getMunicipality(firstDistrictID)['residentsnumber'] == changedValue

    dictChanges =  {'Количество взрослых': changedValue2, 'id': firstDistrictID, 'type': 'Жилое'}
    municipalities.insertChanges(firstDistrictID, dictChanges)
    assert municipalities.getMunicipality(firstDistrictID)['residentsnumber'] == changedValue + changedValue2  

def test_insertChangesSchools():
    dictChanges = {'Количество учеников': changedValue, 'Номинальная вместимость': changedValue2, 'id': firstDistrictID, 'type': 'Школа'}
    dictData = {'currentworkload': 100, 'calculatedworkload': 100}
    municipalities.insertChanges(firstDistrictID, dictChanges, dictData)
    assert round(municipalities.getMunicipality(firstDistrictID)['schoolload']) == 92
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalCapacityDelta'] == changedValue2
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalStudentsDelta'] == changedValue

    dictChanges = {'Количество учеников': changedValue, 'id': firstDistrictID, 'type': 'Школа'}
    municipalities.insertChanges(firstDistrictID, dictChanges, dictData)
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalCapacityDelta'] == changedValue2
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalStudentsDelta'] == changedValue + changedValue

    dictChanges = {'Номинальная вместимость': changedValue2, 'id': firstDistrictID, 'type': 'Школа'}
    municipalities.insertChanges(firstDistrictID, dictChanges, dictData)
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalCapacityDelta'] == changedValue2 + changedValue2
    assert municipalities.getMunicipality(firstDistrictID)['schoolTotalStudentsDelta'] == changedValue + changedValue
