from flask import Flask, render_template, request
# importing the earth engine
import ee
ee.Initialize()
from IPython.display import Image,display
from datetime import date , timedelta
from datetime import datetime
import folium
import pygeoj
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def calculate():
    start_date = '2019-01-01'
    end_date = '2019-04-01'
    data = request.form['data']
    # geometry = request.form['polygon']
    '''a = pygeoj.load(geometry)
    for feature in a:
        roi = (feature.geometry.coordinates)
    region = ee.Geometry.MultiPolygon(roi)
    '''
    def ndvi(start_date,end_date):
        image = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate('2019-01-01','2019-04-10').filterMetadata('CLOUD_COVER','less_than',20).median()
        print(image)
        nir = image.select('B5')
        red = image.select('B4')
        ndvi = nir.subtract(red).divide(nir.add(red))
        viz_parameter = {'min':-0.4,'max':0.5,'palette': ['blue','white','DarkGreen']}
        map_id_dict = ee.Image(ndvi).getMapId(viz_parameter)
        tile = str(map_id_dict['tile_fetcher'].url_format)
        return tile
    def dem():
            image = ee.Image("USGS/SRTMGL1_003")
            viz_parameter = {'min':0,'max':3000,'palette': ['white','black','red']}
            map_id_dict = ee.Image(image).getMapId(viz_parameter)
            tile = str(map_id_dict['tile_fetcher'].url_format)
            print(tile)
        # return "hi i calaculated"
            return tile
    
    def ndbi(start_date,end_date):
            image =  ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate(start_date,end_date).filterMetadata("CLOUD_COVER",'less_than',10).median()
            swir = image.select('B6')
            nir = image.select('B5')
            ndbi = swir.subtract(nir).divide(swir.add(nir))
            viz_parameter = {'min':-0.6,'max':0.2,'palette': ['blue','008000','red']}
            map_id_dict = ee.Image(ndbi).getMapId(viz_parameter)
            tile = str(map_id_dict['tile_fetcher'].url_format)
            return tile
    

    def ndwi(start_date,end_date):
            image =  ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA').filterDate(start_date,end_date).filterMetadata("CLOUD_COVER",'less_than',10).median()
            GREEN = image.select("B3")
            SWIR = image.select("B6")
            ndwi_image = GREEN.subtract(SWIR).divide(GREEN.add(SWIR))#calculate the ndwi
            viz_parameter = {'min':-0.4,'max':0.5,'palette': ['green','red','blue']}
            map_id_dict = ee.Image(ndwi_image).getMapId(viz_parameter)
            tile = str(map_id_dict['tile_fetcher'].url_format)
            print(tile)
            return tile
    
    
    def slope():
            image = ee.Image("USGS/SRTMGL1_003")
            slope = ee.Terrain.slope(image)
            viz_parameter = {'min':0,'max':60,'palette': ['white','black','red']}
            map_id_dict = ee.Image(slope).getMapId(viz_parameter)
            tile = str(map_id_dict['tile_fetcher'].url_format)
            print(tile)
            return tile 
    def lulc():
            return 'hi'

    if (data == 'ndvi'):
        data1 = ndvi(start_date, end_date)
        return render_template('index.html',tiles = data1, title = 'NDVI')
    elif (data == 'ndbi'):
        data1 = ndbi(start_date,end_date)
        return render_template('index.html',tiles=data1, title = 'NDBI')
    elif (data == 'ndwi'):
        data1 = ndwi(start_date,end_date)
        return render_template('index.html',tiles=data1, title = 'NDWI')
    elif(data == 'dem'):
        data1=dem()
        return render_template('index.html',tiles=data1, title = 'DEM')
    elif(data == 'slope'):
        data1 = slope()
        return render_template('index.html',tiles = data1, title = 'SLOPE')
    elif(data == 'lulc'):
        data1 = lulc()
        return render_template('index.html',tiles = data1, title = 'LULCisnotready')
    else:
        data1=dem()
        return render_template('index.html',tiles=data1)
if __name__ == "__main__":
    app.run()