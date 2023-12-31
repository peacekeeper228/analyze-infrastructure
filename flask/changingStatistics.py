from typing import List, Dict, Union

if __package__:
    from .Districts import District
    from .formula import calculateD, calculateP
else:
    from Districts import District
    from formula import calculateD, calculateP


def changeDistrictStatistic(districts_json) -> List[District]:
    listDistricts = []
    for i in range(len(districts_json)):
        dataDistrict = District(districts_json[i])
        
        calculus = calculateD(
            dataDistrict.actualProvisionIndcator,
            dataDistrict.residents,
            dataDistrict.schoolIndex
        )
        oldD = calculus.calculate()

        dataDistrict.updateValues()
        
        calculus = calculateP(
            dataDistrict.residents,
            dataDistrict.schoolIndex,
            oldD + dataDistrict.schoolTotalStudentsDelta - dataDistrict.schoolTotalCapacityDelta
        )
        newP = calculus.calculate()
        dataDistrict.setProvisionIndicator(newP)
        listDistricts.append(dataDistrict)
    return listDistricts

def transformInfoDistricts(districts : List[District] = []) -> List[Dict[str, Union[str, int, float]]]:
    models = {}
    for i in districts:
        territories = i.namedistrict
        models[territories] = {'Площадь (м2)': round(i.area, 0),
            'Количество школ': i.schoolnumber,
            'Средняя загруженность школ(в процентах)': round(i.schoolload, 0),
            'Количество детских садов': i.kindergartennumber,
            'Количество мед учреждений': i.medicinenumber,
            'Количество жилых домов': i.livingnumber,
            'Количество жителей': i.residents,
            'Средний год постройки зданий': i.avgyear,
            'Процент домов, находящихся вне установленной зоны пешей доступности от школ': i.withoutschools,
            'Процент домов, находящихся вне установленной зоны пешей доступности от детских садов': i.withoutkindergartens,
            'Процент домов, находящихся вне установленной зоны пешей доступности от медицинских учреждений': i.withoutmedicine,
            'Количество мест в школах (на 1000 человек)': i.schoolIndex,
            'Удовлетворяет ли количество мест в школах нормативам': ('Нет','Да')[i.schoolProvision],
            'Количество мест в детских садах (на 1000 человек)': i.kindergartenIndex,
            'Удовлетворяет ли количество мест детских садах нормативам': ('Нет','Да')[i.kindergartenProvision],
            'Целевой показатель минимально допустимого уровня обеспеченности населения школами': round(i.targetprovisionindicator, 0),
            'Фактический показатель минимально допустимого уровня обеспеченности населения школами': round(i.actualProvisionIndcator, 0),
            'Плотность жилой застройки': round(i.density, 4)}
    return models

def transformInfoCounties(counties):
    models = {}
    for i in counties:
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
