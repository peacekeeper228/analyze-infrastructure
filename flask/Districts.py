from typing import Dict, List, Set, Union, Tuple
if __package__:
    from .utils import isDisrictProvisionWithSchool, isDistrictProvisionWithKindergarten, calculateNewIndex
else:
    from utils import isDisrictProvisionWithSchool, isDistrictProvisionWithKindergarten, calculateNewIndex

class District(object):
    def __init__(self, data : Dict[str, Union[str, int, float]]) -> None:
        self.data = data

    @property
    def namedistrict(self) -> str:
        return self.data['namedistrict']
    
    @property
    def area(self) -> float:
        return self.data['area']
    
    @property
    def schoolnumber(self) -> int:
        return self.data['schoolnumber']

    @property
    def schoolload(self) -> float:
        return self.data['schoolload']

    @property
    def kindergartennumber(self) -> int:
        return self.data['kindergartennumber']

    @property
    def medicinenumber(self) -> int:
        return self.data['medicinenumber']

    @property
    def livingnumber(self) -> int:
        return self.data['livingnumber']

    @property
    def avgyear(self) -> int:
        return self.data['avgyear']

    @property
    def iddistrict(self) -> str:
        return self.data['iddistrict']
    
    @property
    def schoolIndex(self) -> int:
        return self.data['schoolprovisionindex']
    
    @property
    def kindergartenIndex(self) -> int:
        return self.data['kindergartenprovisionindex']
    
    @property
    def residents(self) -> int:
        return self.data['residentsnumber']
    
    @property
    def density(self) -> float:
        return self.data['density']
    
    @property
    def actualProvisionIndcator(self) -> float:
        return self.data['actualprovisionindicator']
    
    @property
    def targetprovisionindicator(self) -> float:
        return self.data['targetprovisionindicator']
    
    @property
    def schoolTotalCapacityDelta(self) -> int:
        return self.data.get('schoolTotalCapacityDelta', 0)
    
    @property
    def schoolTotalStudentsDelta(self) -> int:
        return self.data.get('schoolTotalStudentsDelta', 0)
    
    @property
    def kinderTotalCapacityDelta(self) -> int:
        return self.data.get('kinderTotalCapacityDelta', 0)
    
    @property
    def rezidentsDelta(self) -> int:
        return self.data.get('residents_delta', 0)
    
    @property
    def schoolProvision(self) -> bool:
        return self.data.get('schoolprovision', 0)
    
    @property
    def kindergartenProvision(self) -> bool:
        return self.data.get('kindergartenprovision', 0)
    
    @property
    def withoutschools(self) -> int:
        return self.data.get('withoutschools', 0)
    
    @property
    def withoutkindergartens(self) -> int:
        return self.data.get('withoutkindergartens', 0)
    
    @property
    def withoutmedicine(self) -> int:
        return self.data.get('withoutmedicine', 0)
    
    def getdata(self) -> Dict[str, Union[str, int, float]]:
        return self.data
    
    def updateValues(self) -> None:
        self.data['residentsnumber'] = self.residents + self.rezidentsDelta

        new_schoolprovisionindex = calculateNewIndex(
            self.schoolIndex,
            self.schoolTotalCapacityDelta,
            self.residents)
        
        new_kindergartenprovisionindex = calculateNewIndex(
            self.kindergartenIndex,
            self.kinderTotalCapacityDelta,
            self.residents)

        self.data['schoolprovisionindex'] = new_schoolprovisionindex
        self.data['kindergartenprovisionindex'] = new_kindergartenprovisionindex
        self.data['schoolprovision'] = isDisrictProvisionWithSchool(self.iddistrict, new_schoolprovisionindex)
        self.data['kindergartenprovision'] = isDistrictProvisionWithKindergarten(self.iddistrict, new_kindergartenprovisionindex)
        
    def setProvisionIndicator(self, actualprovisionindicator : float) -> None:
        self.data['actualprovisionindicator'] = actualprovisionindicator
    