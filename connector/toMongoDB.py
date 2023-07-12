from pymongo import MongoClient
import os

class MongoDB(object):
    def __init__(self):
        self.__client = MongoClient('mongodb',
            username=os.environ['MONGO_LOGIN'],
            password=os.environ['MONGO_PASSWORD'])
    
    def getAllCollections(self):
        d = dict((db, [collection for collection in self.__client[db].list_collection_names()])
            for db in self.__client.list_database_names())
        return d 
   
    def getCentroidAndDAtaByID(self, listvalues, collection):
        db = self.__client['Infrastructure']
        coll = db[collection]
        responselist = list(coll.find({"idSpatial": {"$in": listvalues}}, { "_id": 0}).sort("idSpatial", 1))
        return responselist
    
    def getwithincoordinates(self, poly, collection):
        db = self.__client['Infrastructure']
        coll = db[collection]
        responselist = list(coll.find({ "geometry" : {
            "$geoIntersects": {
            "$geometry": poly
            }}}, { "_id": 0}))
        return responselist
    
    '''
    {
        "type": "Point",
        "coordinates": [37.938057458250945, 55.70359857748261]
    }
    '''

    def getnearcoordinates(self, poly, distance, collection):
        db = self.__client['Infrastructure']
        coll = db[collection]
        responselist = list(coll.find({ "geometry" : {
            "$near" : {
                "$geometry" : poly,
                "$maxDistance" : distance
                }
        }}, { "_id": 0}).sort("idSpatial", 1))
        return responselist
    
    def getnearcoordinateswithdistance(self, poly, distance, collection):
        db = self.__client['Infrastructure']
        coll = db[collection]
        responselist = list(coll.aggregate(
            [{ 
            "$geoNear": { 
                "near" :  poly, 
                "distanceField": "calculated", 
                "maxDistance": distance,  
                "spherical" : True
            }
            },{ "$project" : { "_id" : 0, "geometry": 0} }]))
        return responselist
    