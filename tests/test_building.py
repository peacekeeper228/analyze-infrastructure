import sys
import os
import pytest
import requests
import requests_mock

sys.path.append( os.path.join( os.path.dirname(__file__), ".." ))

from flask.Buildings import BuildingsCollection, LivingBuildings

dataLiving = {'type': 'Жилое', 'id': '1'}
dataSchool = {'type': 'Школа', 'id': '10'}
#since there is no difference between buildings collection, only living is tested
def test_buildings():
    living = LivingBuildings()
    assert living.getDatabaseNumber() == 2
    assert living.getData() == []
    assert living.checkAndInsert(dataLiving) == True
    assert living.getData() == [dataLiving]
    assert living.checkAndInsert(dataSchool) == False
    assert living.getData() == [dataLiving]

    assert living.getDataByID('1') == dataLiving
    with pytest.raises(ValueError):
        living.getDataByID('10')
    with pytest.raises(ValueError):
        living.getDataByID(10)

    assert living.getIDList() == ['1']

def test_buildingObjects():
    living = LivingBuildings()
    living.setObjects([dataLiving, dataSchool])
    assert living.getObjects() == [dataLiving, dataSchool]


def test_insertion():
    buildings = BuildingsCollection()
    data = {'type': 'Жилое', 'id': '12'}
    buildings.insertDataAccordingToType(data)
    assert len(buildings.buildingCollection[0].getData()) == 1

    with pytest.raises(ValueError):
        data = {'type': 'Какой-то странный тип', 'id': '12'}
        buildings.insertDataAccordingToType(data)       