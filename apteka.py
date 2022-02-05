import requests, math


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


def main(address_ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "en_US",
        "ll": address_ll,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        return None
        pass

    json_response = response.json()
    points = []
    for i in range(max(len(json_response["features"]), 10)):
        organization = json_response["features"][i]
        org_time = None
        if "Hours" in organization["properties"]["CompanyMetaData"].keys():
            avai = organization["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]
            for i in avai:
                if "TwentyFourHours" in i.keys():
                    org_time = i["TwentyFourHours"]
                    break
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        points.append((org_point, org_time))
    return points