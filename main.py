from flask import Flask, render_template, request
# importing the earth engine
import ee
ee.Initialize()
from IPython.display import Image,display
import folium
import pygeoj
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def calculate():
    start_date = request.form['startdate']
    end_date = request.form['enddate']
    data = request.form['data']
    # geometry = request.form['polygon']
    '''a = pygeoj.load(geometry)
    for feature in a:
        roi = (feature.geometry.coordinates)
    region = ee.Geometry.MultiPolygon(roi)
    '''
    def ndvi(start_date,end_date):
        
        data1 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA").filterDate(start_date,end_date).sort('CLOUD_COVER').first()
        
        nir = data1.select('B5')
        red = data1.select('B4')
        ndvi_image= nir.subtract(red).divide(nir.add(red))
        vis_params = {"min": -1, "max": 1, "palette": ['blue', 'white', 'green']}
        map_id_dict = ee.Image(ndvi_image).getMapId(vis_params)
        tile = str(map_id_dict['tile_fetcher'].url_format)
        return tile

    if (data == 'ndvi'):
        data1 = ndvi(start_date, end_date)
        return render_template('index.html',tiles = data1)

if __name__ == "__main__":
    app.run(debug = True)