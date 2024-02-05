import requests


def get_static(**params):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=params)
    return response.content


def geocode(toponym_name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_name,
        "format": "json"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Oh no Error', response.status_code, response.reason)
        exit(-1)
    return response.json()


def get_toponym(json_data):
    return json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_toponym_address(toponym):
    address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    try:
        postal = toponym['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    except KeyError:
        postal = None
    return address, postal



def get_toponym_coord(toponym):
    return list(map(float, toponym["Point"]["pos"].split(' ')))


def get_spn(toponym):
    lon1, lat1 = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    lon2, lat2 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    return lon2 - lon1, lat2 - lat1


def search_organisation(**params):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    params['apikey'] = api_key
    response = requests.get(search_api_server, params=params)

    if not response:
        print('Oh no Error', response.status_code, response.reason)
        exit(-1)

    return response.json()


def get_organisation(json_data):
    organization = json_data["features"]
    return organization


def get_org_info(organization):
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_hours = organization["properties"]["CompanyMetaData"]["Hours"]['text']
    return org_name, org_address, org_hours


def get_org_coord(organization):
    point = organization['geometry']['coordinates']
    return point