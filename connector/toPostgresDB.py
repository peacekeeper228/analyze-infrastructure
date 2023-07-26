import psycopg2
import psycopg2.extras
import os
from PostgresPool import PoolConnections
def schooltype():
    return " and t.nameType = 'Школа' "

class MyError(Exception):
    def __init___(self, args):
        Exception.__init__(self, "my exception was raised with arguments {0}".format(args))
        self.args = args

class dbPostgres(object):
    def __init__(self):
        self._pool = PoolConnections()
        self._conn = self._pool.getConnection()
        self._cur = self._conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def _returnDict(self, row):
        if row is not None:
            return(row)
        else:
            raise MyError("no data in DB")
        
    def __del__(self):
        self._pool.returnConnection(self._conn)

class dbPostgresGetCounties(dbPostgres):
    def query(self):
        self._cur.execute("""SELECT namecounty, area, schoolnumber, schoolload,
                kindergartennumber, medicinenumber, livingnumber, residentsnumber, avgyear, withoutschools,
                withoutkindergartens, withoutmedicine from counties ORDER BY namecounty""")
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetDistricts(dbPostgres):
    def query(self):
        self._cur.execute("""SELECT d.namedistrict, c.namecounty, d.area, d.schoolnumber, d.schoolload,
            d.kindergartennumber, d.medicinenumber, d.livingnumber, d.residentsnumber, d.avgyear, d.withoutschools,
            d.withoutkindergartens, d.withoutmedicine, d.schoolProvisionIndex, 
            d.kindergartenProvisionIndex, d.schoolProvision, d.kindergartenProvision from counties c, districts d where c.idCount = d.idCount
            order by c.namecounty, d.namedistrict""")
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
        
class dbPostgresGetDistrictsWithCounyNameByID(dbPostgres):
    def query(self, arrayID):
        SQLquery = """SELECT d.namedistrict, c.namecounty, d.area, d.schoolnumber, d.schoolload,
            d.kindergartennumber, d.medicinenumber, d.livingnumber, d.residentsnumber, d.avgyear, d.withoutschools,
            d.withoutkindergartens, d.withoutmedicine, d.schoolProvisionIndex, 
            d.kindergartenProvisionIndex, d.schoolProvision, d.kindergartenProvision, d.targetProvisionIndicator, 
            d.actualProvisionIndicator, d.density from counties c, districts d
            where c.idCount = d.idCount
            and d.idSpatial in %s
            order by c.namecounty, d.namedistrict"""
        self._cur.execute(SQLquery, (tuple(arrayID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetInCounty(dbPostgres):
    def query(self, county, database, selecttype = ''):
        SQLquery = """SELECT t.* from """ + database + """ t, districts d
            where d.iddistrict = t.iddistrict and d.idcount = %s """ + selecttype + """ ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (county, ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetInDistrict(dbPostgres):
    def query(self, district, database, selecttype = ''):
        if database == 'eduBuildings' and selecttype == schooltype():
            SQLquery = """SELECT t.*, round(currentworkload::float/calculatedworkload * 100) stnumber from """ + database + """ t, districts d
                where d.iddistrict = t.iddistrict and d.nameDistrict in %s """ + selecttype + """ ORDER BY idSpatial"""
        else:
            SQLquery = """SELECT t.* from """ + database + """ t, districts d
                where d.iddistrict = t.iddistrict and d.nameDistrict in %s """ + selecttype + """ ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(district), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetBySpatialID(dbPostgres):
    def query(self, arrayID, database):
        SQLquery = """SELECT t.* from """ + database + """ t
            where t.idSpatial in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(arrayID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetByID(dbPostgres):
    def query(self, arrayID, database):
        SQLquery = """SELECT t.* from """ + database + """ t
            where t.buildid in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(arrayID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetByIDWithCountyID(dbPostgres):
    def query(self, arrayID, database):
        SQLquery = """SELECT t.*, d.idcount from """ + database + """ t, districts d
                where d.iddistrict = t.iddistrict
            and t.buildid in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(arrayID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetDistrictsByName(dbPostgres):
    def query(self, nameID):
        SQLquery = """SELECT namedistrict, area, idspatial, schoolnumber, schoolload,
            kindergartennumber, medicinenumber, livingnumber, residentsnumber, avgyear, withoutschools,
            withoutkindergartens, withoutmedicine, schoolProvisionIndex, 
            kindergartenProvisionIndex, schoolProvision, kindergartenProvision, targetProvisionIndicator, 
            actualProvisionIndicator, density from districts where nameDistrict in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(nameID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetDistrictsByNameWithID(dbPostgres):
    def query(self, nameID):
        SQLquery = """SELECT iddistrict, namedistrict, area, idspatial, schoolnumber, schoolload,
            kindergartennumber, medicinenumber, livingnumber, residentsnumber, avgyear, withoutschools,
            withoutkindergartens, withoutmedicine, schoolProvisionIndex, 
            kindergartenProvisionIndex, schoolProvision, kindergartenProvision, targetProvisionIndicator, 
            actualProvisionIndicator, density from districts where nameDistrict in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(nameID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetDistrictsByID(dbPostgres):
    def query(self, nameID):
        SQLquery = """SELECT namedistrict, area, idspatial, schoolnumber, schoolload,
            kindergartennumber, medicinenumber, livingnumber, residentsnumber, avgyear, withoutschools,
            withoutkindergartens, withoutmedicine, schoolProvisionIndex, 
            kindergartenProvisionIndex, schoolProvision, kindergartenProvision, targetProvisionIndicator, 
            actualProvisionIndicator, density from districts where idDistrict in %s ORDER BY idSpatial"""
        self._cur.execute(SQLquery, (tuple(nameID), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetCountybyIDdistrict(dbPostgres):
    def query(self, idDistrict):
        SQLquery = """
            SELECT c.namecounty, c.area, c.schoolnumber, c.schoolload, c.kindergartennumber, c.medicinenumber, c.livingnumber, c.residentsnumber, c.avgyear, c.withoutschools, c.withoutkindergartens, c.withoutmedicine
            FROM counties c, districts d
            WHERE d.idcount = c.idcount and d.iddistrict = %s
            ORDER BY namecounty"""
        self._cur.execute(SQLquery, (idDistrict,))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetCountybyDistrictName(dbPostgres):
    def query(self, NameDistrict):
        SQLquery = """SELECT c.namecounty, c.area, c.schoolnumber, c.schoolload,
    c.kindergartennumber, c.medicinenumber, c.livingnumber, c.residentsnumber, c.avgyear, c.withoutschools,
    c.withoutkindergartens, c.withoutmedicine from counties c, districts d where d.idcount = c.idcount and d.namedistrict = %s ORDER BY namecounty"""

        self._cur.execute(SQLquery, (NameDistrict,))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())
    
class dbPostgresGetCountiesByName(dbPostgres):
    def query(self, arrayName):
        SQLquery = """SELECT idcount, namecounty, area, schoolnumber, schoolload,
            kindergartennumber, medicinenumber, livingnumber, residentsnumber, avgyear, withoutschools,
            withoutkindergartens, withoutmedicine from counties where namecounty in %s ORDER BY namecounty"""
        self._cur.execute(SQLquery, (tuple(arrayName), ))
        self._conn.commit()
        return self._returnDict(self._cur.fetchall())