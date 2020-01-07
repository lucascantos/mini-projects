
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json

def make_feature(coordinates, geometry="Polygon"):
    singleFeature = {
        "type": "Feature",
        "geometry": {
            "type": geometry,
        },
        "properties": {}
    }

    if geometry == 'GeometryCollection':
        singleFeature['geometry']['geometries'] = coordinates
    else:
        singleFeature['geometry']['coordinates'] = coordinates

    return singleFeature

def unpack_kmz(file):
    kmz = ZipFile(file, 'r')
    kml = kmz.open('doc.kml', 'r')
    kmlText = kml.read().decode()

    with open('output.kml', "w") as f:
        f.write(kmlText)


kmz_file = '5_areas_atuacao.kmz'
kml_file = 'output.kml'

tree = ET.parse(kml_file)
root = tree.getroot()

regions = root.findall('Folder')
client_region = {
    "type": "FeatureCollection",
    "features": []
}

for region in regions:
    region_name = region.find('name').text
    cities = region.findall('Document')
    region_geometry = []
    for city in cities:
        city_name = region.find('name').text
        trails = city.findall('Folder')
        coords = city.iter("coordinates")
        city_geometry = []
        for coord in coords:
            text = coord.text
            text = text.replace('\t', '')
            text = text.replace('\n', '')

            first_coord = text.split(' ')[0]
            first_coord = first_coord.split(',')[:2]

            lon = float(first_coord[0])
            lat = float(first_coord[1])

            first_coord = [lon, lat]

            city_geometry.append(first_coord)
        region_geometry.append({
           "type": "LineString",
           "coordinates": city_geometry
            })

    region_geojson = make_feature(region_geometry, 'GeometryCollection')
    region_geojson['properties']['name'] = region_name
    client_region['features'].append(region_geojson)


with open('output.json', 'w') as f:
    json.dump(client_region, f)
    # if len(child)>0:
    #     region = child
    #     print(region.find('name').text)
    #     cities = region.findall('Document')
    #     print(cities)
