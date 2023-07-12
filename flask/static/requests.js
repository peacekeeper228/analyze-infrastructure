function sendRequestForChanges(data, districts) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/checkchanges', true); // false for synchronous request
        let body = JSON.stringify({
            data: data,
            districts: districts
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}

function sendRequestForChanges_county(data, counties) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/checkchanges_county', true); // false for synchronous request
        let body = JSON.stringify({
            data: data,
            counties: counties
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}

function sendRequestToDefineChangesForSchool(changedSchools) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/checkforschool', true); // false for synchronous request
        let body = JSON.stringify(changedSchools);
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}

function sendRequestHexagones(districtsArray, hexsizevalue) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/hexForDistricts', true); // false for synchronous request
        body = JSON.stringify({
            "IDsource": districtsArray,
            "hexagone_size": parseInt(hexsizevalue)
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}

function sendRequestDistricts(districtsArray) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/districtsfullinfo', true); // false for synchronous request
        let body = JSON.stringify({
            "IDsource": districtsArray
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}

function sendRequestNearCoordinates(lat, lon, buildingType) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/nearcoordinates', true); // false for synchronous request
        let body = JSON.stringify({
            "lat": lat,
            "lon": lon,
            "database": buildingType
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                resolve(textJSON);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}


function sendRequestBuildingsInDistricts(districtsArray, builddatabase) {
    return new Promise(function (resolve, reject) {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST", 'http://127.0.0.1:80/buildingfullinfo', true); // false for synchronous request
        body = JSON.stringify({
            "IDsource": districtsArray,
            "isCounty": false,
            "database": builddatabase
        });
        xmlHttp.onload = function () {
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                textJSON = xmlHttp.responseText;
                let res = JSON.parse(textJSON);
                resolve(res);
            } else {
                reject(xmlHttp.status);
            }
        };
        xmlHttp.send(body);
    });
}