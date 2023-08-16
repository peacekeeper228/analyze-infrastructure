import sys
import os

sys.path.append( os.path.join( os.path.dirname(__file__), "..." ))
from flask.changingStatistics import changeDistrictStatistic, transformInfoCounties, transformInfoDistricts

AllValues1 = {
    'namedistrict' : 'Название района',
    'area': 123.4,
    'schoolnumber': 56,
    'schoolload' : 234.5,
    'kindergartennumber': 123,
    'medicinenumber': 234,
    'livingnumber': 345,
    'avgyear': 456,
    'iddistrict': 'relation/1281220',
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
    'schoolprovision': False,
    'kindergartenprovision': False,
    'withoutschools': 3456,
    'withoutkindergartens': 4567,
    'withoutmedicine': 5678
}

def test_changeDistrictStatistic():
    changedDistricts = changeDistrictStatistic([AllValues1])
    assert len(changedDistricts) == 1
    district = changedDistricts[0]
    assert district.schoolProvision == True
    assert district.kindergartenProvision == True
    assert district.actualProvisionIndcator == 2684.237
    assert district.residents == 3134
    assert district.schoolIndex == 850
    assert district.kindergartenIndex == 1071


AllValues2 = {
    'namedistrict' : 'Название района',
    'area': 123.4,
    'schoolnumber': 56,
    'schoolload' : 234.5,
    'kindergartennumber': 123,
    'medicinenumber': 234,
    'livingnumber': 345,
    'avgyear': 456,
    'iddistrict': 'relation/1281220',
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
    'schoolprovision': False,
    'kindergartenprovision': False,
    'withoutschools': 3456,
    'withoutkindergartens': 4567,
    'withoutmedicine': 5678
}
districtsForFrontend = {
    'Название района':{'Площадь (м2)':123.0,
    'Количество школ': 56,
    'Средняя загруженность школ(в процентах)': 234.0,
    'Количество детских садов': 123,
    'Количество мед учреждений': 234,
    'Количество жилых домов': 345,
    'Количество жителей': 3134,
    'Средний год постройки зданий': 456,
    'Процент домов, находящихся вне установленной зоны пешей доступности от школ': 3456,
    'Процент домов, находящихся вне установленной зоны пешей доступности от детских садов': 4567,
    'Процент домов, находящихся вне установленной зоны пешей доступности от медицинских учреждений': 5678,
    'Количество мест в школах (на 1000 человек)': 850,
    'Удовлетворяет ли количество мест в школах нормативам': 'Да',
    'Количество мест в детских садах (на 1000 человек)': 1071,
    'Удовлетворяет ли количество мест детских садах нормативам': 'Да',
    'Целевой показатель минимально допустимого уровня обеспеченности населения школами': 568.0,
    'Фактический показатель минимально допустимого уровня обеспеченности населения школами': 2684.0,
    'Плотность жилой застройки': 345.6}
}
def test_transformInfoDistricts():
    changedDistricts = changeDistrictStatistic([AllValues2])
    models = transformInfoDistricts(changedDistricts)
    assert models == districtsForFrontend

AllValues3 = {
    'namecounty': 'Название округа',
    'area': 123.4,
    'schoolnumber': 123,
    'schoolload': 234.5,
    'kindergartennumber': 234,
    'medicinenumber': 345,
    'livingnumber': 456,
    'residentsnumber': 567,
    'avgyear': 678,
    'withoutschools': 789,
    'withoutkindergartens' : 890,
    'withoutmedicine': 901
}
countiesForFrontend = {
    'Название округа':{
    'Площадь (м2)': 123.0,
    'Количество школ': 123,
    'Средняя загруженность школ(в процентах)': 234.0,
    'Количество детских садов': 234,
    'Количество мед учреждений': 345,
    'Количество жилых домов': 456,
    'Количество жителей': 567,
    'Средний год постройки зданий': 678,
    'Процент домов,находящихся вне установленной зоны пешей доступности от школ': 789,
    'Процент домов,находящихся вне установленной зоны пешей доступности от детских садов': 890,
    'Процент домов,находящихся вне установленной зоны пешей доступности от медицинских учреждений': 901}
}
def test_transformInfoCounties():
    assert transformInfoCounties([AllValues3]) == countiesForFrontend