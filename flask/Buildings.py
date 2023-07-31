from typing import List, Dict, Union
class InfoBuildings(object):
    _typeOfBuilding = ''
    _databaseNumber = 0
    def __init__(self) -> None:
        self._listID = []
        self._json = []

    def __insertData(self, data : Dict[str, Union[str, int, float]]) -> None:
        self._json.append(data)
        self._listID.append(data['id'])

    def getIDList(self) -> List[str]:
        return self._listID
    
    def getDatabaseNumber(self) -> int:
        return self._databaseNumber
    
    def checkAndInsert(self, data : Dict[str, Union[str, int, float]]) -> bool:
        if data['type'] == self._typeOfBuilding:
            self.__insertData(data)
            return True
        return False
    
    def getData(self) -> List[Dict[str, Union[str, int, float]]]:
        return self._json
    
    def getDataByID(self, buildid : str) -> Dict[str, Union[str, int, float]]:
        for i in self._json:
            if i['id'] == buildid:
                return i
        raise ValueError("Объект с таким идентификатором не найден")
    
    def setObjects(self, data : List[Dict[str, Union[str, int, float]]]) -> None:
        self.__objects = data

    def getObjects(self) -> List[Dict[str, Union[str, int, float]]]:
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
    def insertDataAccordingToType(self, data : Dict[str, Union[str, int, float]]) -> None:
        for i in self.buildingCollection:
            if i.checkAndInsert(data):
                return
        raise ValueError("type of building is undefined " + data['type'])