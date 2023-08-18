conn = new Mongo();
db = conn.getDB('Infrastructure');
db.counties.createIndex({ 'geometry': '2dsphere' });
db.counties.createIndex({ 'idSpatial': 1 });
db.counties.insertMany([{
    "idSpatial": 9,
    "geometry": {
        "coordinates": [
            [
                [
                    37.522703107126375,
                    55.88016256094454
                ],
                [
                    37.41352672426814,
                    55.78147953719014
                ],
                [
                    37.500526654357316,
                    55.63731816081909
                ],
                [
                    37.67964415748196,
                    55.60842202574514
                ],
                [
                    37.800761707214974,
                    55.7142704213025
                ],
                [
                    37.71205589614368,
                    55.838995238411
                ],
                [
                    37.522703107126375,
                    55.88016256094454
                ]
            ]
        ],
        "type": "Polygon"
    }
}]);

conn = new Mongo();
db = conn.getDB('Infrastructure');
db.districts.createIndex({ 'geometry': '2dsphere' });
db.districts.createIndex({ 'idSpatial': 1 });
db.districts.insertMany([
    {
        "idSpatial": 106,
        "geometry": {
            "coordinates": [
                [
                    [
                        37.54252803014498,
                        55.852040922091476
                    ],
                    [
                        37.479410433807004,
                        55.75424645248697
                    ],
                    [
                        37.63464560318215,
                        55.65909322330842
                    ],
                    [
                        37.73699846211025,
                        55.77152215216498
                    ],
                    [
                        37.54252803014498,
                        55.852040922091476
                    ]
                ]
            ],
            "type": "Polygon"
        }
    }]);

conn = new Mongo();
db = conn.getDB('Infrastructure');
db.livingBuildings.createIndex({ 'geometry': '2dsphere' });
db.livingBuildings.createIndex({ 'idSpatial': 1 });
db.livingBuildings.insertMany([
    {
        "idSpatial": 4499, "latitude": 55.81332, "longitude": 37.457336, "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        37.457336,
                        55.81332
                    ],
                    [
                        37.463928,
                        55.7775
                    ],
                    [
                        37.551819,
                        55.779971
                    ],
                    [
                        37.547424,
                        55.808382
                    ],
                    [
                        37.457336,
                        55.81332
                    ]
                ]
            ]
        }
    }]);
conn = new Mongo();
db = conn.getDB('Infrastructure');
db.medBuildings.createIndex({ 'geometry': '2dsphere' });
db.medBuildings.createIndex({ 'idSpatial': 1 });
db.medBuildings.insertMany([{
    "idSpatial": 618, "latitude": 55.781207, "longitude": 37.573792, "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    37.573792,
                    55.781207
                ],
                [
                    37.573792,
                    55.75154
                ],
                [
                    37.648499,
                    55.746594
                ],
                [
                    37.641907,
                    55.789856
                ],
                [
                    37.573792,
                    55.781207
                ]
            ]
        ]
    }
}]);
conn = new Mongo();
db = conn.getDB('Infrastructure');
db.eduBuildings.createIndex({ 'geometry': '2dsphere' });
db.eduBuildings.createIndex({ 'idSpatial': 1 });
db.eduBuildings.insertMany([
    {
        "idSpatial": 1, "latitude": 55.814555, "longitude": 37.547424, "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        37.547424,
                        55.814555
                    ],
                    [
                        37.547424,
                        55.779971
                    ],
                    [
                        37.600159,
                        55.779971
                    ],
                    [
                        37.593567,
                        55.808382
                    ],
                    [
                        37.547424,
                        55.814555
                    ]
                ]
            ]
        }
    },
    {
        "idSpatial": 8, "latitude": 55.6994881258353, "longitude": 37.92327313473727, "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        37.731995,
                        55.81332
                    ],
                    [
                        37.731995,
                        55.793562
                    ],
                    [
                        37.795715,
                        55.792326
                    ],
                    [
                        37.786926,
                        55.819493
                    ],
                    [
                        37.731995,
                        55.81332
                    ]
                ]
            ]
        }
    },
]);