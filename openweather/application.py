from flask import Flask, render_template, abort, request, redirect
import json
import os
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/' + request.form.get('zones') + '?' + 'lang=' + request.form.get('lang'))
    areas = next(os.walk('data/zones/'))[1]
    data_to_render = {}
    for area in areas:
        area_data = {}
        with open('data/zones/' + area + '/' + area + '.txt', encoding='utf-8') as data:
            area_data = json.load(data)
        data_to_render[area_data['name']] = area
    print(data_to_render)
    return render_template('home.html', zones=data_to_render)

@app.route('/<string:zone>')
def widget(zone):
    try:
        lang = 'es'
        if request.args.get('lang', ''):
            lang = request.args.get('lang', '')
        datafile = 'data/zones/' + zone + '/' + zone + '.txt'
        area_data = {}
        with open(datafile, encoding='utf-8') as data:
            area_data = json.load(data)
        lat = area_data['latitude']
        lng = area_data['longitude']
        name = area_data['name']

        return render_template('widget.html', lat=lat, lng=lng, zone=name, lang=lang)
    except:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('errors/404.html'), 404

# start the server
if __name__ == '__main__':
    app.run(debug=True)