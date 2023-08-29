import requests
from typing import List
import os, sys
import json
sys.path.append(os.getcwd())
if __package__:
    from .Municipality import Municipalities
    from .utils import docker_net
else:
    from Municipality import Municipalities
    from utils import docker_net
    
def requestBuildingsFullInfo(database : int, arrayID : List[int]) -> List[dict]:
    try:
        jsonData = requests.post(f'{docker_net}buildingIDcounty', json={"database": database, "arrayID" : arrayID}).json()
        return jsonData
    except ValueError:
        raise ValueError("Во время запроса к серверу что-то пошло не так")
    
def getSpatialIDDistrictByCoordinates(lon : float, lat : float) -> int:
    try:
        jsonData = requests.post(f'{docker_net}pointInDistrict', json={"lon" : lon, "lat": lat}).json()
        districtID = jsonData[0]["idSpatial"]
        return districtID
    except:
        raise ValueError("Во время запроса к серверу что-то пошло не так")
    
def infoAboutSelectedDistricts(selectedDistricts: List[str]) -> Municipalities:
    dist_post_json = {
        "IDsource": selectedDistricts
    }
    full_selected_districts = requests.post(f'{docker_net}districtsinfobyname', json=dist_post_json).json()
    return Municipalities(full_selected_districts)

def infoAboutSelectedCounties(selectedDistricts: List[str]) -> Municipalities:
    county_post_json = {
        "countynames": selectedDistricts
    }
    full_selected_districts = requests.post(f'{docker_net}countyinfobynames', json=county_post_json).json()
    for i in range(len(full_selected_districts)):
        full_selected_districts[i]['iddistrict'] = full_selected_districts[i]['idcount']
        del full_selected_districts[i]['idcount']
    return Municipalities(full_selected_districts)

def mapInfo() -> dict:
    r = requests.get(f'{docker_net}districtcountyname')
    return json.loads(r.text)
    