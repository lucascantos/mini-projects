
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json
import re
from unidecode import unidecode

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
kml_file = 'output/output.kml'

def decode_kml(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()

    regions = root.findall('Folder')

    # DECODE KML
    client_data = []
    for region in regions:
        region_data = {
            "properties": {},
            "cities": []
        }
        region_name = region.find('name').text
        region_data['properties']['name'] = region_name

        cities = region.findall('Document')
        for city in cities:
            city_data = {
                "properties":{},
                "geometry": []
            }

            city_name = city.find('name').text
            city_data['properties']['name'] = city_name

            trails = city.findall('Folder')
            coords = city.iter("coordinates")
            # print(city_name)
            for coord in coords:
                text = coord.text
                text = text.replace('\t', '')
                text = text.replace('\n', '')

                points = text.split(' ')[:2]
                for i, point in enumerate(points):
                    point = point.split(',')[:2]
                    for j, coord in enumerate(point):
                        point[j] = float(coord)
                    points[i] = point
                city_data['geometry'].append(points)
            region_data['cities'].append(city_data)
        client_data.append(region_data)
    return {"regions": client_data}

coprel_data = decode_kml(kml_file)
with open('output/output.json', 'w') as f:
    json.dump(coprel_data, f)

def encode_json(regions_file):

    cities_geojson_file = 'inputs/municipios.json'
    with open(cities_geojson_file) as f:
        cities_geojson = json.load(f)
    

    with open(regions_file) as f:
        regions_data = json.load(f)

    city_features = {
        'label': [],
        'geometry': []
    }

    #Grabing geometry of cities
    for feature in cities_geojson['features']:

        label = feature['properties']['Label_N']

        city_features['label'].append(unidecode(label))
        city_features['geometry'].append(feature['geometry'])
    
    regions_collection = {
        "type": "FeatureCollection",
        "features": []
    }  

    for region in regions_data['regions']:
        city_geometries = []

        print(region['properties']['name'].upper())
        for city in region['cities']:
            city_name = city['properties']['name']
            print(city_name)

            city_index = city_features['label'].index(unidecode(city_name))
            city_geometry = city_features['geometry'][city_index]
            city_geometries.append(city_geometry)

            # Making the GeoJson
        region_feature = {
            "type": "Feature",
            "properties":region['properties'],
            "geometry": {
                "type": "GeometryCollection",
                "geometries": city_geometries
            }}
        regions_collection['features'].append(region_feature)

        return regions_collection

    # region_data.append({
    #     "type": "LineString",
    #     "coordinates": points
    #     })
    # POLYGON
    # first_coord = text.split(' ')[0]
    # first_coord = first_coord.split(',')[:2]

    # lon = float(first_coord[0])
    # lat = float(first_coord[1])

    # first_coord = [lon, lat]

    #     city_data.append(first_coord)
    # city_data.append(city_data[0])
    # region_data.append({
    #    "type": "LineString",
    #    "coordinates": city_data
    #     })

    # region_geojson = make_feature(region_data, 'GeometryCollection')
    # region_geojson['properties']['name'] = region_name
    # client_region['features'].append(region_geojson)


regions_file = 'output/output.json'
regions_collection = encode_json(regions_file)

with open('output/area_atuacao2.json', 'w') as f:
    json.dump(regions_collection, f)
