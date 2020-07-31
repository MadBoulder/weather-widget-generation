from flask import Flask, render_template
import json
app = Flask(__name__)

@app.route('/<string:zone>')
def widget(zone):
    datafile = 'data/zones/' + zone + '/' + zone + '.txt'
    area_data = {}
    with open(datafile, encoding='utf-8') as data:
        area_data = json.load(data)
    lat = area_data['latitude']
    lng = area_data['longitude']
    name = area_data['name']

    return render_template('widget.html', lat=lat, lng=lng, zone=name, lang='es')

# start the server
if __name__ == '__main__':
    app.run(debug=True)