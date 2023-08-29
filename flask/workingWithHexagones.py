import h3
def assembleHexagones(data : dict, hexagoneSize : int) -> list:
    hexagones = []
    for i in range(len(data['features'])):
        featureHexagones = createHexagons(data['features'][i]['geometry'], hexagoneSize)
        hexagones.extend(featureHexagones)
    return hexagones

def createHexagons(geometry : dict, hexagoneSize : int):
    hexagones = []
    if geometry['type'] == 'Polygon':
        hexagones = list(h3.polyfill(geometry, hexagoneSize))
    elif geometry['type'] == 'MultiPolygon':
        for i in geometry['coordinates']:
            artificialPolygon = {"type": "Polygon", "coordinates": i}
            hexagones.extend(list(h3.polyfill(artificialPolygon, hexagoneSize)))
    return hexagones