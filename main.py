import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image, ImageDraw, ImageFont
from apteka import main, lonlat_distance

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    sys.exit()
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
apteka_info = main(toponym_coodrinates.replace(' ', ','))
pts = {None: ',pmgrm', False: ',pmblm', True: ',pmgnm'}
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
    "l": "map",
    "pt": toponym_coodrinates.replace(' ', ',') + ',pma~' +
          '~'.join(i[0] + pts[i[1]] for i in apteka_info)
}
response = requests.get(map_api_server, params=map_params)
image = Image.open(BytesIO(response.content))
image.show()