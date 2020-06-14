import urllib.request
import urllib.parse
import json

A_TAG = """
<a 
    class="weatherwidget-io" 
    href="https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/" 
    data-label_1="_LOCATION_PRETTY_" data-label_2="WEATHER" 
    data-theme="pure"
>
    _LOCATION_PRETTY_ WEATHER
</a>
"""

SCRIPT = """
<script>
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
</script>
"""


def get_coordinates(location):
    location = location.replace(" ", "+")
    api_key = None
    with open("credentials.txt", "r", encoding='utf-8') as f:
        api_key = f.read()
    query_url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(
        location, api_key)
    inp = urllib.request.urlopen(query_url)
    coords = json.load(inp)['results'][0]['geometry']
    coords['lat'] = round(coords['lat'], 2)
    coords['lng'] = round(coords['lng'], 2)
    return coords


def format_coordinates(coordinates):
    lat = str(coordinates['lat'])
    if lat[::-1].find('.') == 1:
        lat += "0"
    lat = lat.replace(".", "d")
    lat = lat.replace("-", "n")
    lng = str(coordinates['lng'])
    if lng[::-1].find('.') == 1:
        lng += "0"
    lng = lng.replace(".", "d")
    lng = lng.replace("-", "n")
    return lat + lng


def get_widget_code(coords, location, pretty_location, lang):
    tag = A_TAG.replace("_COORDS_", coords)
    tag = tag.replace("_LOCATION_PRETTY_", pretty_location)
    tag = tag.replace("_LOCATION_", location)
    tag = tag.replace("_LANG_", lang)
    return tag


def main():
    location = "Valencia, Spain"
    pass


if __name__ == "__main__":
    coords = get_coordinates("Sant Joan de Vilatorrada, Spain")
    formated_coords = format_coordinates(coords)
    # print(formated_coords)
    tag_code = get_widget_code(
        formated_coords,
        "sant-joan-de-vilatorrada",
        "Sant Joan de Vilatorrada",
        "es")
    with open("template.html", "a") as f:
        f.write(tag_code + SCRIPT)

    # main()
