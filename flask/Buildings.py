from typing import List
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
    
    def setObjects(self, data):
        self.__objects = data

    def getObjects(self):
        return self.__objects

class LivingBuildings(InfoBuildings):
    _typeOfBuilding = 'Жилое'
    _databaseNumber = 2

class SchoolBuildings(InfoBuildings):
    _typeOfBuilding = 'Школа'
    _databaseNumber = 0

class KindergartenBuildings(InfoBuildings):
    _typeOfBuilding = 'Детский сад'
    _databaseNumber = 3

class BuildingsCollection(object):
    buildingCollection: List[InfoBuildings]
    def __init__(self) -> None:
        self.buildingCollection = [
            LivingBuildings(),
            SchoolBuildings(),
            KindergartenBuildings()
        ]
    def insertDataAccordingToType(self, data) -> None:
        for i in self.buildingCollection:
            if i.checkAndInsert(data):
                return
        raise ValueError("type of building is undefined " + i['type'])
    
