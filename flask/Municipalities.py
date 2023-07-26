class Municipalities(object):
    _districtsID = set()
    _districts = []

    def __init__(self, data : dict) -> None:
        self._districts = data
        self._districtsID = set([i['iddistrict'] for i in data])

    def insertID(self, id):
        self._districtsID.add(id)

    def getMunicipality(self, districtID):
        for i in self._districts:
            if districtID == i['iddistrict']:
                return i
            
    def getNumberMunicipality(self, districtID):
        for i in range(len(self._districts)):
            if districtID == self._districts[i]['iddistrict']:
                return i
    
    def getMunicipalitiesID(self):
        return self._districtsID
    
    def checkInMunicipalities(self, idDistrict):
        return idDistrict in self._districtsID
    
    def getMunicipalities(self):
        return self._districts
    
    def returnDict(self):
        dictDistricts = {}
        keys = ['iddistrict']
        for i in self._districts:
            dictDistricts[i['iddistrict']] = {k: v for k, v in i.items() if k not in keys}
    
    def insertChanges(self, districtID, dictChanges, dictData):
        NumberInArray = self.getNumberMunicipality(districtID)
        if dictChanges['type'] == 'Детский сад':
            self._districts[NumberInArray]['kinderTotalCapacityDelta'] = self._districts[NumberInArray].get('kinderTotalCapacityDelta', 0) + dictChanges.get('Номинальная вместимость', 0)
        if dictChanges['type'] == 'Жилое':
            self._districts[NumberInArray]['residentsnumber'] = self._districts[NumberInArray].get('residentsnumber', 0) + dictChanges.get('Количество взрослых', 0)
        if dictChanges['type'] == 'Школа':
            self._districts[NumberInArray]['schoolTotalCapacityDelta'] = self._districts[NumberInArray].get('schoolTotalCapacityDelta', 0) + dictChanges.get('Номинальная вместимость', 0)
            self._districts[NumberInArray]['schoolTotalStudentsDelta'] = self._districts[NumberInArray].get('schoolTotalStudentsDelta', 0) + dictChanges.get('Количество учеников', 0)
            oldWorkloadInSchool = calculateWorkloadInSchool(dictData['currentworkload'], dictData['calculatedworkload'])
            newWorkloadInSchool = calculateWorkloadInSchool(dictData['currentworkload'] + dictChanges.get("Количество учеников", 0), dictData['calculatedworkload'] + dictChanges.get("Номинальная вместимость", 0))
            self._districts[NumberInArray]['schoolload'] = changeWorkloadInDistrict(
                self._districts[NumberInArray]['schoolnumber'],
                self._districts[NumberInArray]['schoolload'],
                oldWorkloadInSchool,
                newWorkloadInSchool)

def changeWorkloadInDistrict(numberOfSchoolsInDistrict, averageSchoolLoadInDistrict, oldWorkloadInSchool, newWorkloadInSchool):
    oldTotalWorkloadInDistrict = numberOfSchoolsInDistrict * averageSchoolLoadInDistrict
    newAverageSchoolLoadInDistrict = (oldTotalWorkloadInDistrict - oldWorkloadInSchool + newWorkloadInSchool) / numberOfSchoolsInDistrict
    return newAverageSchoolLoadInDistrict

def calculateWorkloadInSchool(numberOfStudents, schoolCapacity):
    return (numberOfStudents / schoolCapacity) * 100