import urllib.request
import urllib.parse
import json
import http.client

TOLERANCE = 5

A_TAG = """
<a 
    class="weatherwidget-io" 
    href="https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/" 
    data-label_1="_LOCATIONPRETTY_" data-label_2="WEATHER" 
    data-theme="pure"
>
    _LOCATIONPRETTY_ WEATHER
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
    return coords


def format_coordinates(coordinates):
    coordinates['lat'] = round(coordinates['lat'], 2)
    coordinates['lng'] = round(coordinates['lng'], 2)
    lat = str(coordinates['lat'])
    if lat[::-1].find('.') == 1:
        lat += "0"
    lat = lat.replace(".", "d").replace("-", "n")
    lng = str(coordinates['lng'])
    if lng[::-1].find('.') == 1:
        lng += "0"
    lng = lng.replace(".", "d").replace("-", "n")
    return lat + lng


def get_widget_code(coords, location, pretty_location, lang):
    tag = A_TAG.replace("_COORDS_", coords)
    tag = tag.replace("_LOCATIONPRETTY_", pretty_location)
    tag = tag.replace("_LOCATION_", location)
    tag = tag.replace("_LANG_", lang)
    url = "https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/"
    url = url.replace("_COORDS_", coords).replace(
        "_LOCATION_", location).replace("_LANG_", lang)
    return tag, url


def is_url_ok(url):
    try:
        req = urllib.request.Request(
            url, headers={'User-Agent': "Magic Browser"})
        urllib.request.urlopen(req)
        return True
    except:
        return False


def main():
    pass


if __name__ == "__main__":
    url_name = "chironico"
    pretty_name = "Chironico"
    coords = get_coordinates("Chironico, Switzerland")
    formated_coords = format_coordinates(coords)
    print(formated_coords)
    # print(formated_coords)
    tag_code, url = get_widget_code(
        formated_coords,
        url_name,
        pretty_name,
        "es")
    if is_url_ok(url):
        with open("template.html", "a") as f:
            f.write(tag_code + SCRIPT)
    else:
        print("Failed")
        if TOLERANCE:
            for i in range(TOLERANCE):
                print(i)
                nc = coords['lat'] + i/100
                for j in range(TOLERANCE):
                    ncl = coords['lng'] + j/100
                    formated_coords = format_coordinates(
                        {'lat': nc, 'lng': ncl})
                    print(formated_coords)
                    tag_code, url = get_widget_code(
                        formated_coords,
                        url_name,
                        pretty_name,
                        "es")
                    if is_url_ok(url):
                        print("Fixed")
                        with open("template.html", "a") as f:
                            f.write(tag_code + SCRIPT)
                    ncl = coords['lng'] - j/100
                    formated_coords = format_coordinates(
                        {'lat': nc, 'lng': ncl})
                    print(formated_coords)
                    tag_code, url = get_widget_code(
                        formated_coords,
                        url_name,
                        pretty_name,
                        "es")
                    if is_url_ok(url):
                        print("Fixed")
                        with open("template.html", "a") as f:
                            f.write(tag_code + SCRIPT)

                nc = coords['lat'] - i/100
                for j in range(TOLERANCE):
                    ncl = coords['lng'] + j/100
                    formated_coords = format_coordinates(
                        {'lat': nc, 'lng': ncl})
                    print(formated_coords)
                    tag_code, url = get_widget_code(
                        formated_coords,
                        url_name,
                        pretty_name,
                        "es")
                    if is_url_ok(url):
                        print("Fixed")
                        with open("template.html", "a") as f:
                            f.write(tag_code + SCRIPT)

                    ncl = coords['lng'] - j/100
                    formated_coords = format_coordinates(
                        {'lat': nc, 'lng': ncl})
                    print(formated_coords)
                    tag_code, url = get_widget_code(
                        formated_coords,
                        url_name,
                        pretty_name,
                        "es")
                    if is_url_ok(url):
                        print("Fixed")
                        with open("template.html", "a") as f:
                            f.write(tag_code + SCRIPT)

    # main()
