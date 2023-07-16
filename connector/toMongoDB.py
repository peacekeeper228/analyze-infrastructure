from pymongo import MongoClient
import os

class dbMongo(object):
    def __init__(self):
        self._client = MongoClient('mongodb',
            username=os.environ['MONGO_LOGIN'],
            password=os.environ['MONGO_PASSWORD'])
    def _getDatabase(self):
        return self._client['Infrastructure']
    
    def _getCollection(self, collectionName):
        db = self._getDatabase()
        return db[collectionName]
        
class dbMongoGetAllCollections(dbMongo):
    def query(self):
        d = dict((db, [collection for collection in self._client[db].list_collection_names()])
            for db in self._client.list_database_names())
        return d
    
class dbMongoGetCentroidAndDAtaByID(dbMongo):
    def query(self, listvalues, collection):
        coll = self._getCollection(collection)
        responselist = list(coll.find({"idSpatial": {"$in": listvalues}}, { "_id": 0}).sort("idSpatial", 1))
        return responselist
    
class dbMongoGetWithinCoordinates(dbMongo):
    def query(self, poly, collection):
        coll = self._getCollection(collection)
        responselist = list(coll.find({ "geometry" : {
            "$geoIntersects": {
            "$geometry": poly
            }}}, { "_id": 0}))
        return responselist

class dbMongoGetNearCoordinates(dbMongo):
    def query(self, poly, distance, collection):
        coll = self._getCollection(collection)
        responselist = list(coll.find({ "geometry" : {
            "$near" : {
                "$geometry" : poly,
                "$maxDistance" : distance
                }
        }}, { "_id": 0}).sort("idSpatial", 1))
        return responselist
    
class dbMongoGetNearCoordinatesWithDistance(dbMongo):
    def query(self, poly, distance, collection):
        coll = self._getCollection(collection)
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
    


    