function selectMarkedDistricts() {
    let districts = document.getElementsByClassName('inner');
    let districtsArray = [];
    for (var i = 0; i < districts.length; ++i) {
        var item = districts[i];
        if (item.checked) {
            districtsArray.push(item.id);
        }
    }
    if (districtsArray.length == 0) {
        throw new RangeError('Районы не выбраны');
    };
    return districtsArray;
}

function selectMarkedCounties() {
    let counties = document.getElementsByClassName('outer');
    let countiesArray = [];
    for (var i = 0; i < counties.length; ++i) {
        var item = counties[i];
        if (item.checked) {
            countiesArray.push(item.id.slice(0, -1));
        }
    }
    if (countiesArray.length == 0) {
        throw new RangeError('Округа не выбраны');
    };
    return countiesArray;
}

function selectMarkedBuildings() {
    builddatabaseCheck = document.querySelector('input[name="buldtype"]:checked');
    if (!builddatabaseCheck) {
        throw new RangeError('Тип зданий не выбран');
    };
    return builddatabaseCheck.value;
}

function selectMarkedHexSize() {
    let hexsize = document.querySelector('input[name="hexsize"]:checked');
    if (!hexsize) {
        throw new RangeError('Размер гексагона не задан');
    };
    return hexsize.value;
}