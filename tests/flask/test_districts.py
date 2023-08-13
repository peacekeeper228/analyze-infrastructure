import sys
import os
import pytest

sys.path.append( os.path.join( os.path.dirname(__file__), "..." ))
from flask.Districts import District

dictData = {
    'iddistrict' : 'relation/1281220',
    'schoolprovisionindex' : 12.0,
    'kindergartenprovisionindex' : 13.0,
    'residentsnumber': 10000,
    'actualprovisionindicator' : 12.0,
    'schoolprovision' : False,
    'kindergartenprovision' : False
}
dataDistrict = District(dictData)

def test_data():
    assert dataDistrict.getdata() == dictData

def test_updateValuesWithNoChanges():
    dataDistrict.updateValues()
    assert dataDistrict.schoolIndex == 12.0
    assert dataDistrict.kindergartenIndex == 13.0
    assert dataDistrict.residents == 10000
    assert dataDistrict.schoolProvision == False
    assert dataDistrict.kindergartenProvision == False

def test_updateValuesWithChanges():
    dictData['schoolTotalCapacityDelta'] = 1234
    dictData['schoolTotalStudentsDelta'] = 234
    dictData['kinderTotalCapacityDelta'] = 567
    dictData['residents_delta'] = 1000
    districtWithChanges = District(dictData)
    districtWithChanges.updateValues()
    assert districtWithChanges.residents == 11000
    assert districtWithChanges.schoolIndex == 124
    assert districtWithChanges.kindergartenIndex == 64
    assert districtWithChanges.schoolProvision == True
    assert districtWithChanges.kindergartenProvision == True

def test_setProvisionIndicator():
    dataDistrict.setProvisionIndicator(15.0)
    assert dataDistrict.actualProvisionIndcator == 15.0

AllValues = {
    'namedistrict' : 'namedistrict',
    'area': 123.4,
    'schoolnumber': 56,
    'schoolload' : 234.5,
    'kindergartennumber': 123,
    'medicinenumber': 234,
    'livingnumber': 345,
    'avgyear': 456,
    'iddistrict': 'iddistrict',
    'schoolprovisionindex': 567,
    'kindergartenprovisionindex': 678,
    'residentsnumber': 789,
    'density': 345.6,
    'actualprovisionindicator': 456.7,
    'targetprovisionindicator': 567.8,
    'schoolTotalCapacityDelta': 890,
    'schoolTotalStudentsDelta': 901,
    'kinderTotalCapacityDelta': 1234,
    'residents_delta': 2345,
    'schoolprovision': True,
    'kindergartenprovision': False,
    'withoutschools': 3456,
    'withoutkindergartens': 4567,
    'withoutmedicine': 5678
}

def test_districtProperties():
    dataDistrict = District(AllValues)
    assert dataDistrict.namedistrict == 'namedistrict'
    assert dataDistrict.area == 123.4
    assert dataDistrict.schoolnumber == 56
    assert dataDistrict.schoolload == 234.5
    assert dataDistrict.kindergartennumber == 123
    assert dataDistrict.medicinenumber == 234
    assert dataDistrict.livingnumber == 345
    assert dataDistrict.avgyear == 456
    assert dataDistrict.iddistrict == 'iddistrict'
    assert dataDistrict.schoolIndex == 567
    assert dataDistrict.kindergartenIndex == 678
    assert dataDistrict.residents == 789
    assert dataDistrict.density == 345.6
    assert dataDistrict.actualProvisionIndcator == 456.7
    assert dataDistrict.targetprovisionindicator == 567.8
    assert dataDistrict.schoolTotalCapacityDelta == 890
    assert dataDistrict.schoolTotalStudentsDelta == 901
    assert dataDistrict.kinderTotalCapacityDelta == 1234
    assert dataDistrict.rezidentsDelta == 2345
    assert dataDistrict.schoolProvision == True
    assert dataDistrict.kindergartenProvision == False
    assert dataDistrict.withoutschools == 3456
    assert dataDistrict.withoutkindergartens == 4567
    assert dataDistrict.withoutmedicine == 5678

