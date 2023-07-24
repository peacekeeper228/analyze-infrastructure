class InfoBuildings(object):
    _typeOfBuilding = ''
    _databaseNumber = 0
    def __init__(self) -> None:
        self._listID = []
        self._json = []

    def insertData(self, data):
        self._json.append(data)
        self._listID.append(data['id'])

    def getIDList(self):
        return self._listID
    
    def getDatabaseNumber(self):
        return self._databaseNumber
    
    def checkAndInsert(self, data):
        if data['type'] == self._typeOfBuilding:
            self.insertData(data)
            return True
        return False
    
    def getData(self):
        return self._json
    
    def getDataByID(self, buildid):
        for i in self._json:
            if i['id'] == buildid:
                return i

class LivingBuildings(InfoBuildings):
    _typeOfBuilding = 'Жилое'
    _databaseNumber = 2

class SchoolBuildings(InfoBuildings):
    _typeOfBuilding = 'Школа'
    _databaseNumber = 0

class KindergartenBuildings(InfoBuildings):
    _typeOfBuilding = 'Детский сад'
    _databaseNumber = 3

class Districts(object):
    _districtsID = set()
    _districts = []

    def __init__(self, data : dict) -> None:
        self._districts = data
        self._districtsID = set([i['iddistrict'] for i in data])

    def insertID(self, id):
        self._districtsID.add(id)

    def getDistrict(self, districtID):
        for i in self._districts:
            if districtID == i['iddistrict']:
                return i
            
    def getNumberDistrict(self, districtID):
        for i in range(len(self._districts)):
            if districtID == self._districts[i]['iddistrict']:
                return i
    
    def getDistrictsID(self):
        return self._districtsID
    
    def checkInDistricts(self, idDistrict):
        return idDistrict in self._districtsID
    
    def getDistricts(self):
        return self._districts
    
    def returnDict(self):
        dictDistricts = {}
        keys = ['iddistrict']
        for i in self._districts:
            dictDistricts[i['iddistrict']] = {k: v for k, v in i.items() if k not in keys}
    
    def insertChanges(self, districtID, dictChanges, dictData):
        NumberInArray = self.getNumberDistrict(districtID)
        if dictChanges['type'] == 'Детский сад':
            self._districts[NumberInArray]['kinderTotalCapacityDelta'] = self._districts[NumberInArray].get('kinderTotalCapacityDelta', 0) + dictChanges.get('Номинальная вместимость', 0)
        
        #self._districts[districtID]['schoolTotalCapacityDelta'] += dictChanges.get('Загруженность (в процентах от номинальной)', 0)
        #self._districts[NumberInArray]['kinderTotalCapacityDelta'] = self._districts[NumberInArray].get('kinderTotalCapacityDelta', 0) + dictChanges.get('Номинальная вместимость', 0)
        if dictChanges['type'] == 'Жилое':
            self._districts[NumberInArray]['residentsnumber'] = self._districts[NumberInArray].get('residentsnumber', 0) + dictChanges.get('Количество взрослых', 0)
        if dictChanges['type'] == 'Школа':
            self._districts[NumberInArray]['schoolTotalCapacityDelta'] = self._districts[NumberInArray].get('schoolTotalCapacityDelta', 0) + dictChanges.get('Номинальная вместимость', 0)
            self._districts[NumberInArray]['schoolTotalStudentsDelta'] = self._districts[NumberInArray].get('schoolTotalStudentsDelta', 0) + dictChanges.get('Количество учеников', 0)
            self._districts[NumberInArray]['schoolload'] = change_schools_workload(self._districts[NumberInArray]['schoolnumber'],
                                                            self._districts[NumberInArray]['schoolload'],
                                    dictData['currentworkload'], dictData['calculatedworkload'],
                                    dictChanges.get("Количество учеников", 0), dictChanges.get("Номинальная вместимость", 0))
        
def change_schools_workload(dist_school_number, dist_school_load, old_number, old_capacity, new_number, new_capacity):
    total_workload = dist_school_number * dist_school_load
    school_old_workload = (old_number / old_capacity * 100)
    without_one_school_workload = total_workload - school_old_workload
    school_new_workload = ((old_number + new_number) / (old_capacity +new_capacity) * 100)
    total_workload = (without_one_school_workload + school_new_workload) / dist_school_number
    return total_workload