class Dictionary(object):
    @staticmethod
    def getRusNameOrEngDefault(engName: str) -> str:
        return dictfromdatabase.get(engName, engName)
    @staticmethod
    def translateDictKeysRusThrows(engDict: dict, throwKeys: list) -> dict:
        return {Dictionary.getRusNameOrEngDefault(x): engDict[x] for x in engDict if x not in throwKeys}
    @staticmethod
    def translateListRus(engList: list) -> list:
        return [Dictionary.getRusNameOrEngDefault(x) for x in engList]   
    def getRusNameOrException(engname):
        pass
dictfromdatabase = {'adress': 'Адрес',
    'adults': 'Количество взрослых',
    'area': 'Площадь (м2)',
    'availablekindergartens': 'Кол-во дет. садов в R-доступности',
    'availablemedicine': 'Кол-во мед. учреждений в R-доступности',
    'availableschools': 'Кол-во школ в R-доступности',
    'avgyear': 'Средний год постройки',
    'buildid': 'Идентификатор',
    'buildyear': 'Год постройки',
    'calculatedworkload': 'Номинальная вместимость',
    'children': 'Количество детей',
    'currentworkload':'Количество учеников',
    'freeschools': 'Количество свободных школ',
    'fullname': 'Название',
    'idSpatial': 'ГеоИдентификатор',
    'kinder': 'Количество детских садов',
    'kinder_index':'Процент домов,находящихся вне установленной зоны пешей доступности от детских садов',
    'kindergartennumber': 'Количество дс',
    'kindergartenprovision': 'Обеспеченность дс*',
    'kindergartenprovisionindex': 'Индекс обеспеченности дс',
    'latitude': 'Широта',
    'livingnumber': 'Количество жилых домов',
    'longitude': 'Долгота',
    'medicine':'Количество мед учреждений',
    'medicine_index': 'Процент домов,находящихся вне установленной зоны пешей доступности от медицинских учреждений',
    'medicinenumber': 'Количество мед. учреждений',
    'namecount': 'Название округа',
    'namedistrict': 'Название района',
    'pupils': 'Количество школьников',
    'rating': 'Рейтинг',
    'residents': 'Количество жителей',
    'residentsnumber': 'Количество жильцов',
    'school_index': 'Процент домов,находящихся вне установленной зоны пешей доступности от школ',
    'schoolload': 'Средняя загрузка школ',
    'schoolnumber': 'Количество школ',
    'schoolprovision': 'Обеспеченность школами*',
    'schoolprovisionindex': 'Индекс обеспеченности школ',
    'schools': 'Количество школ',
    'stnumber': 'Загруженность (в процентах от номинальной)',
    'storey': 'Этажность',
    'year': 'Средний год постройки зданий',
    'website': 'Сайт',
    'withoutkindergartens': 'хз дс',
    'withoutmedicine': 'хз мед',
    'withoutschools': 'хз школ'
}

notUsedTypes = [
    'geometry',
    'flats',
    'idspatial', 
    'eoid',
    'storey',
    'totalarea'
    'website']

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

zone_1 = ['relation/1281220', 'relation/1250526', 'relation/1257484', 'relation/446079', 'relation/2162195',
    'relation/445298',
    'relation/1281648', 'relation/444908', 'relation/446114', 'relation/1255942', 'relation/952191',
    'relation/1257218',
    'relation/240229', 'relation/1281702', 'relation/1252407', 'relation/364001', 'relation/1278046',
    'relation/1292499',
    'relation/1250619', 'relation/1299106', 'relation/1275551', 'relation/1292679', 'relation/446115',
    'relation/446272',
    'relation/445281', 'relation/445280', 'relation/364551', 'relation/1275608', 'relation/1257786',
    'relation/1292731',
    'relation/446112', 'relation/1255987', 'relation/428431', 'relation/445299', 'relation/1281263',
    'relation/1275627']
zone_2 = ['relation/1252465', 'relation/1319060', 'relation/1252424', 'relation/446078', 'relation/1255704',
    'relation/445297',
    'relation/1319142', 'relation/1281209', 'relation/1292286', 'relation/1319263', 'relation/1319245',
    'relation/445277',
    'relation/1292211', 'relation/444812', 'relation/226927', 'relation/442741', 'relation/445273',
    'relation/1278064',
    'relation/1252448', 'relation/1250724', 'relation/455222', 'relation/1319078', 'relation/442733',
    'relation/1257472',
    'relation/445283', 'relation/455528', 'relation/535655', 'relation/455460', 'relation/535662',
    'relation/1298976',
    'relation/455539', 'relation/456807', 'relation/445282', 'relation/1292749', 'relation/1299013',
    'relation/446081',
    'relation/1250618', 'relation/1255680', 'relation/446086', 'relation/445279', 'relation/1299031',
    'relation/434560',
    'relation/455184', 'relation/445276', 'relation/446111', 'relation/445274', 'relation/950641',
    'relation/535680',
    'relation/951305', 'relation/950664', 'relation/431464', 'relation/446087', 'relation/446080',
    'relation/1278096',
    'relation/446271', 'relation/951334']

zone_3 = ['relation/181288', 'relation/380702', 'relation/380703', 'relation/380704', 'relation/380705',
    'relation/380706', 'relation/380707', 'relation/380708', 'relation/445275', 'relation/445278',
    'relation/445284', 'relation/445285', 'relation/446082', 'relation/446083', 'relation/446084',
    'relation/446085', 'relation/446116', 'relation/446117', 'relation/455203', 'relation/455208',
    'relation/455451', 'relation/531264', 'relation/531287', 'relation/548619', 'relation/574667',
    'relation/950639', 'relation/950658', 'relation/951336', 'relation/1255563', 'relation/1255576',
    'relation/1255577', 'relation/1255602', 'relation/1257403', 'relation/1257455', 'relation/1320371',
    'relation/1320424', 'relation/1320510', 'relation/1320566', 'relation/1320570', 'relation/1668007',
    'relation/1693596', 'relation/1693661', 'relation/1693667', 'relation/1693672', 'relation/1703093',
    'relation/1703095', 'relation/2092922', 'relation/2092924', 'relation/2092925', 'relation/2092927',
    'relation/2092928', 'relation/2092929', 'relation/2092931']

school_zone_1 = 105
school_zone_2 = 112
school_zone_3 = 124
kinder_zone_1 = 46
kinder_zone_2 = 55
kinder_zone_3 = 63

def schooltype():
    return " and t.nameType = 'Школа' "

def kindergartentype():
    return " and t.nameType = 'Детский сад' "

valuesdict = {
    1:'Количество школ',
    3:'Количество детских садов',
    4:'Количество мед учреждений',
    6:'Количество жителей',
    7:'Год постройки зданий',
    0:'Площадь',
    8:'Процент домов вне зоны пешей доступности от школ',
    9:'Процент домов вне зоны пешей доступности от детских садов',
    10:'Процент домов вне зоны пешей доступности от мед учреждений',
    2:'Средняя загрузка школ',
    11:'Количество мест в школах (на 1000 человек)',
    13:'Количество мест в детских садах (на 1000 человек)'
}
valuescounty = {
    0:'Площадь',
    1:'Количество школ',
    3:'Количество детских садов',
    4:'Количество мед учреждений',
    5:'Количество жилых домов',
    6:'Количество жителей',
    7:'Год постройки зданий',
    8:'Процент домов вне зоны пешей доступности от школ',
    9:'Процент домов вне зоны пешей доступности от детских садов',
    10:'Процент домов вне зоны пешей доступности от мед учреждений',
    2:'Средняя загруженность школ'

}

docker_net = "http://connector:8000/"
#out_net = "http://127.0.0.1:8008/"
#docker_net = "http://127.0.0.1:8008/"