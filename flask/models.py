import requests
import json
from typing import List
from .Municipality import Municipalities

from .utils import docker_net
def requestBuildingsFullInfo(database : int, arrayID : List[int]) -> List[dict]:
    try:
        jsonData = requests.post(docker_net + "buildingIDcounty", json={"database": database, "arrayID" : arrayID}).json()
        if jsonData == []:
            raise ValueError("У нас нет инфомации о данном объекте")
        return jsonData
    except:
        raise ValueError("У нас нет инфомации о данном объекте")
    

def getSpatialIDDistrictByCoordinates(lon : float, lat : float) -> int:
    try:
        jsonData = requests.post(docker_net + "pointInDistrict", json={"lon" : lon, "lat": lat}).json()
        districtID = jsonData[0]["idSpatial"]
        return districtID
    except:
        raise ValueError("Выбранный объект не принадлежит ни одному району")
    
def infoAboutSelectedDistricts(selectedDistricts: List[str]) -> Municipalities:
    dist_post_json = {
        "IDsource": selectedDistricts
    }
    full_selected_districts = requests.post(docker_net + "districtsinfobyname", json=dist_post_json).json()
    return Municipalities(full_selected_districts)

def infoAboutSelectedCounties(selectedDistricts: List[str]) -> Municipalities:
    county_post_json = {
        "countynames": selectedDistricts
    }
    full_selected_districts = requests.post(docker_net + "countyinfobynames", json=county_post_json).json()
    for i in range(len(full_selected_districts)):
        full_selected_districts[i]['iddistrict'] = full_selected_districts[i]['idcount']
        del full_selected_districts[i]['idcount']
    return Municipalities(full_selected_districts)
    