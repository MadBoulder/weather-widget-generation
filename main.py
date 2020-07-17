import urllib.request
import urllib.parse
import json
import http.client

TOLERANCE = 5

A_TAG = """
<a 
    class="weatherwidget-io big-widget" 
    href="https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/" 
    data-label_1="_LOCATIONPRETTY_" data-label_2="WEATHER" 
    data-font="Roboto" data-theme="pure"
>
    _LOCATIONPRETTY_ {{_("WEATHER")}}
</a>
"""

# For mobile we only show the forecast for 3 days
A_TAG_MOBILE = """
<a 
    class="weatherwidget-io small-widget" 
    href="https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/" 
    data-label_1="_LOCATIONPRETTY_" data-label_2="WEATHER" 
    data-font="Roboto" data-mode="Forecast" 
    data-days="3" data-theme="pure" 
>
    _LOCATIONPRETTY_ {{_("WEATHER")}}
</a>
"""

SCRIPT = """
<script>
!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';fjs.parentNode.insertBefore(js,fjs);}}(document,'script','weatherwidget-io-js');
</script>
"""


def get_widget_for_area(area, lang="en"):
    """
    """
    datafile = 'data/zones/' + area + '/' + area + '.txt'
    area_data = {}
    with open(datafile, 'r', encoding='utf-8') as data:
        area_data = json.load(data)
    if area_data.get('weather_location'):
        widget_code = get_widget_html(area_data.get(
            'weather_location'), lang=lang, units=None, formated_coords=area_data.get("weather_coords"))
    return widget_code


def get_coordinates(location):
    """
    Given a location, retrieve its latitude and longitude
    coordinates via opencagedata API
    """
    location = urllib.parse.quote(location.replace(" ", "+"))
    api_key = None
    with open("credentials.txt", "r", encoding='utf-8') as f:
        api_key = f.read()
    query_url = "https://api.opencagedata.com/geocode/v1/json?q={}&key={}".format(
        location, api_key)
    inp = urllib.request.urlopen(query_url)
    coords = json.load(inp)['results'][0]['geometry']
    return coords


def format_coordinates(coordinates):
    """
    Given a set of coordinates in the form {'lat': LAT, 'lng': LNG}
    format them to weatherwidget.io expected url coordinate format.
    The format is:
    - coordinates rounded to 2nd decimal
    - dots replaced by d
    - minus signs replaced by n
    - LAT and LNG concatenated
    """
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


def normalize(s):
    replacements = (
        ("á", "a"),
        ("à", "a"),
        ("é", "e"),
        ("è", "e"),
        ("é", "e"),
        ("í", "i"),
        ("ì", "i"),
        ("ó", "o"),
        ("ò", "o"),
        ("ú", "u"),
        ("ù", "u"),
        ("ñ", "n")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def get_url_location_name(location):
    """
    Transform the location name used to search the coordinates into
    the location format used in weatherwidget.io widget url
    """
    return normalize(location.split(",")[0].lower().replace(" ", "-"))


def get_widget_code(coords, pretty_location, lang):
    """
    Generate the a tag of the widget from the retrieved info
    """
    location = get_url_location_name(pretty_location)
    tag = A_TAG.replace("_COORDS_", coords)
    tag = tag.replace("_LOCATIONPRETTY_", pretty_location)
    tag = tag.replace("_LOCATION_", location)
    tag = tag.replace("_LANG_", lang)
    url = "https://forecast7.com/_LANG_/_COORDS_/_LOCATION_/"
    url = url.replace("_COORDS_", coords).replace(
        "_LOCATION_", location).replace("_LANG_", lang)
    print(url)
    return tag, url


def is_url_ok(url):
    """
    Test if the weatherwidget.io generated url is valid
    """
    try:
        req = urllib.request.Request(
            url, headers={'User-Agent': "Magic Browser"})
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        print(e)
        return False


def fix_url(coords, pretty_name, lang):
    if TOLERANCE:
        for i in range(-TOLERANCE, TOLERANCE + 1):
            nc = coords['lat'] + i/100
            for j in range(-TOLERANCE, TOLERANCE + 1):
                ncl = coords['lng'] + j/100
                formated_coords = format_coordinates(
                    {'lat': nc, 'lng': ncl})
                tag_code, url = get_widget_code(
                    formated_coords,
                    pretty_name,
                    lang)
                if is_url_ok(url):
                    return tag_code, url


def get_widget_html(pretty_name, lang, units=None, formated_coords=None):
    if formated_coords is None:
        coords = get_coordinates(pretty_name)
        formated_coords = format_coordinates(coords)
    tag_code, url = get_widget_code(
        formated_coords,
        pretty_name,
        lang)
    if not is_url_ok(url):
        tag_code, url = fix_url(coords, pretty_name, lang)
    with open("template.html", "a") as f:
        f.write(tag_code + SCRIPT)
    return tag_code + SCRIPT


if __name__ == "__main__":
    # Commented lines are areas that already work 
    # get_widget_for_area('albarracin')
    # get_widget_for_area('alcaniz')
    # get_widget_for_area('ailefroide')
    # get_widget_for_area('annot')
    # get_widget_for_area('arboli')
    # get_widget_for_area('bagni_di_masino')  # 46d249d60
    # get_widget_for_area('bezas')
    # get_widget_for_area('brione') # 46d308d79
    # get_widget_for_area('bergkristall') # 46d8011d09
    # get_widget_for_area('bullenheimer_berg')
    get_widget_for_area('can_barto')
