import sys
import os
import pytest
import requests
import requests_mock

sys.path.append( os.path.join( os.path.dirname(__file__), ".." ))
from flask.models import requestBuildingsFullInfo, getSpatialIDDistrictByCoordinates, infoAboutSelectedCounties, infoAboutSelectedDistricts
from flask.utils import docker_net
from flask.Municipality import Municipalities

def test_GetInformationAboutBuilding(requests_mock):
    requests_mock.post(f'{docker_net}buildingIDcounty', json=['aa'])
    resp = requestBuildingsFullInfo(2, [[1, 2, 3]])
    assert resp == ['aa']

    with pytest.raises(ValueError):
        requests_mock.post(f'{docker_net}buildingIDcounty', json=[])
        resp = requestBuildingsFullInfo(2, [[1, 2, 3]])

def test_getSpatialIDDistrictByCoordinates(requests_mock):
    requests_mock.post(f'{docker_net}pointInDistrict', json=[{'idSpatial': '10'}])
    resp = getSpatialIDDistrictByCoordinates(1.0, 2.0)
    assert resp == '10'

    with pytest.raises(ValueError):
        requests_mock.post(f'{docker_net}pointInDistrict', json=[])
        resp = getSpatialIDDistrictByCoordinates(1.0, 2.0)

def test_infoAboutSelectedDistricts(requests_mock):
    info = [{'iddistrict': '10', 'schoolnumber': 15}]
    requests_mock.post(f'{docker_net}districtsinfobyname', json=info)
    municipality = infoAboutSelectedDistricts('10')
    assert municipality.getMunicipalities() == info
    assert municipality.getMunicipalitiesID() == set(['10'])

def test_infoAboutSelectedCounties(requests_mock):
    info = [{'idcount': '10', 'schoolnumber': 15}]
    expectedInfo = [{'iddistrict': '10', 'schoolnumber': 15}]
    requests_mock.post(f'{docker_net}countyinfobynames', json=info)
    municipality = infoAboutSelectedCounties('10')
    assert municipality.getMunicipalities() == expectedInfo
    assert municipality.getMunicipalitiesID() == set(['10'])