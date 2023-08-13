--lookup tebles

CREATE TABLE eduTypes
(
    nameType CHARACTER VARYING(11) PRIMARY KEY
);

CREATE TABLE medTypes
(
    nameType CHARACTER VARYING(20) PRIMARY KEY
);

CREATE TABLE zones
(
    name CHARACTER VARYING(20) PRIMARY KEY
    schoolValue INTEGER,
    kindergartenValue INTEGER
);

--basic tables

CREATE TABLE counties
(
    idCount CHARACTER VARYING(100) PRIMARY KEY,
    nameCounty CHARACTER VARYING(100),
    idSpatial INTEGER,
    area REAL,
    schoolNumber INTEGER,
    schoolLoad REAL,
    kindergartenNumber INTEGER,
    medicineNumber INTEGER,
    livingNumber INTEGER,
    residentsNumber INTEGER,
    avgYear INTEGER,
    withoutSchools INTEGER,
    withoutKindergartens INTEGER,
    withoutMedicine INTEGER
);

CREATE TABLE districts
(
    idDistrict CHARACTER VARYING(100) PRIMARY KEY,
    nameDistrict CHARACTER VARYING(100),
    idSpatial INTEGER,
    idCount CHARACTER VARYING(100) REFERENCES counties (idCount),
    area REAL,
    schoolNumber INTEGER,
    schoolLoad REAL,
    kindergartenNumber INTEGER,
    medicineNumber INTEGER,
    livingNumber INTEGER,
    residentsNumber INTEGER,
    avgYear INTEGER,
    withoutSchools INTEGER,
    withoutKindergartens INTEGER,
    withoutMedicine INTEGER,
    schoolProvisionIndex INTEGER,
    kindergartenProvisionIndex INTEGER,
    schoolProvision BOOLEAN,
    kindergartenProvision BOOLEAN,
    targetProvisionIndicator REAL,
    actualProvisionIndicator REAL,
    density REAL
);

CREATE TABLE eduBuildings
(
    buildID SERIAL PRIMARY KEY,
    fullName CHARACTER VARYING(200),
    shortName CHARACTER VARYING(100),
    website CHARACTER VARYING(100),
    adress CHARACTER VARYING(200),
    area REAL,
    storey INTEGER,
    calculatedWorkload INTEGER,
    currentWorkload INTEGER,
    totalArea REAL,
    idSpatial INTEGER,
    rating REAL,
    eoid INTEGER,
    idDistrict CHARACTER VARYING(100) REFERENCES districts (idDistrict),
    nameType CHARACTER VARYING(11) REFERENCES eduTypes (nameType)
);

CREATE TABLE medBuildings
(
    buildID SERIAL PRIMARY KEY,
    fullName CHARACTER VARYING(200),
    website CHARACTER VARYING(200),
    adress CHARACTER VARYING(200),
    area REAL,
    storey INTEGER,
    idSpatial INTEGER,
    medType CHARACTER VARYING(20) REFERENCES medTypes (nameType),
    idDistrict CHARACTER VARYING(100) REFERENCES districts (idDistrict)
);

CREATE TABLE livingBuildings
(
    buildID SERIAL PRIMARY KEY,
    adress CHARACTER VARYING(200),
    flats INTEGER,
    area REAL,
    storey INTEGER,
    buildYear INTEGER,
    children INTEGER,
    pupils INTEGER,
    adults INTEGER,
    freeSchools INTEGER,
    availableSchools INTEGER,
    availableKindergartens INTEGER,
    availableMedicine INTEGER,
    idSpatial INTEGER,
    idDistrict CHARACTER VARYING(100) REFERENCES districts (idDistrict)
);