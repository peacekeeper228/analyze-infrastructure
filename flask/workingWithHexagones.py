import h3
def assembleHexagones(data, hexagone_size):
    polylines_list = []
    for i in range(len(data['features'])):
        polylinet = createHexagons(data['features'][i], hexagone_size)
        polylines_list.extend(polylinet)
    return polylines_list

def createHexagons(data, hexagone_size):
    sub_geoJson = data['geometry']
    hexagons = []
    if sub_geoJson['type'] == 'Polygon':
        hexagons = list(h3.polyfill(sub_geoJson, hexagone_size))
    else:
        for i in sub_geoJson['coordinates']:
            sub_sub = {"type": "Polygon", "coordinates": i}
            hexagons.extend(list(h3.polyfill(sub_sub, hexagone_size)))
    return hexagons