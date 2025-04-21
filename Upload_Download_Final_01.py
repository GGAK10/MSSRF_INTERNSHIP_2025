import ee
import time
import requests
import threading
import webbrowser
from flask import Flask, request, jsonify
from waitress import serve
from tqdm import tqdm
from datetime import datetime
import folium
import zipfile
import os
import shutil
import geopandas as gpd
import geemap.foliumap as geemap
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = Flask(__name__)

# Earth Engine Auth
ee.Authenticate()
ee.Initialize(project='bb-kagg09160')

# Default ROI (Chennai)
roi = ee.Geometry.Polygon([[
    [80.19640081183177, 12.982156617399665],
    [80.2753650452302, 12.982156617399665],
    [80.2753650452302, 13.030995739701355],
    [80.19640081183177, 13.030995739701355],
    [80.19640081183177, 12.982156617399665]
]])

# Placeholder
ndvi, classified, image = None, None, None

def process_layers():
    global image, ndvi, classified, Map

    image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(roi) \
        .filterDate('2022-01-01', '2025-02-28') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1)) \
        .select(['B2', 'B3', 'B4', 'B8', 'B11']) \
        .median() \
        .clip(roi)

    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    #classified = image.select('B4')  # Placeholder classified layer
    bands = image.select(['B2', 'B3', 'B4', 'B8','B11'])

#***************************************************************************************************************************************
    Sand = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([80.27230130132146, 13.001071062573054]),
            {
              "Class": 1,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([80.1515152853021, 13.21316196552836]),
            {
              "Class": 1,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([79.67638185072731, 13.259064262169817]),
            {
              "Class": 1,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([79.50603961675336, 13.32218119977785]),
            {
              "Class": 1,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([79.48259342667808, 13.317827520586887]),
            {
              "Class": 1,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([79.6282962967801, 12.994110127428478]),
            {
              "Class": 1,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([79.62649134246358, 12.988858284060104]),
            {
              "Class": 1,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([78.11000223114571, 11.065082617798643]),
            {
              "Class": 1,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([77.1531904026712, 8.251354932442306]),
            {
              "Class": 1,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([77.1551672395625, 8.249808148495875]),
            {
              "Class": 1,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([77.16384236606314, 8.24351533509495]),
            {
              "Class": 1,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([77.17736652971122, 8.22979944049614]),
            {
              "Class": 1,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([77.4953834125616, 8.08678083269935]),
            {
              "Class": 1,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([77.57621104455042, 8.13580246261975]),
            {
              "Class": 1,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([77.59112693125543, 8.142784398159563]),
            {
              "Class": 1,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([77.76513546068921, 8.192926497638368]),
            {
              "Class": 1,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([77.79569968763721, 8.231835354999086]),
            {
              "Class": 1,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([77.80056039146436, 8.238396747834665]),
            {
              "Class": 1,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([77.80948031451847, 8.243763121934366]),
            {
              "Class": 1,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([77.82646007480372, 8.249515223890235]),
            {
              "Class": 1,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([77.90155448698704, 8.286194300135632]),
            {
              "Class": 1,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([77.95388401327631, 8.320145882783846]),
            {
              "Class": 1,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([78.43069329982173, 9.712751322128403]),
            {
              "Class": 1,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([79.27024170701173, 10.9912631513809]),
            {
              "Class": 1,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([79.42287721442906, 11.10669553695892]),
            {
              "Class": 1,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([79.61763183279149, 11.259045267425428]),
            {
              "Class": 1,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([79.7208781793679, 11.35652077535441]),
            {
              "Class": 1,
              "system:index": "26"
            })])
    Water_Bodies = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([80.2146874239677, 12.987876152429067]),
            {
              "Class": 2,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([80.21511402115284, 13.223079001916783]),
            {
              "Class": 2,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([80.1957241346181, 13.235194182510666]),
            {
              "Class": 2,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([80.1500889040136, 13.236632071114615]),
            {
              "Class": 2,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([80.14566111414713, 13.222873022134882]),
            {
              "Class": 2,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([80.15302462955307, 13.146367481506571]),
            {
              "Class": 2,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([80.13241609786027, 13.160920448436501]),
            {
              "Class": 2,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([80.04090621740801, 13.17941721651484]),
            {
              "Class": 2,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([80.03500141746717, 13.177124666156692]),
            {
              "Class": 2,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([80.04316450385677, 13.142526289973636]),
            {
              "Class": 2,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([79.912813241803, 13.140210253046764]),
            {
              "Class": 2,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([79.50432593141169, 13.281342699152713]),
            {
              "Class": 2,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([79.50358575145898, 13.281884525274732]),
            {
              "Class": 2,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([79.4345017184822, 13.259959376487847]),
            {
              "Class": 2,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([79.44468048265917, 13.16898579318796]),
            {
              "Class": 2,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([79.66203316596379, 13.045741653835144]),
            {
              "Class": 2,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([79.64802348779835, 13.046647748410711]),
            {
              "Class": 2,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([79.6293485702133, 13.005149932146594]),
            {
              "Class": 2,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([79.62943335582091, 13.007460855300746]),
            {
              "Class": 2,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([79.55041875758816, 12.928239344783163]),
            {
              "Class": 2,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([76.9396987890659, 11.003801690324044]),
            {
              "Class": 2,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([76.94117096244194, 11.003698132540501]),
            {
              "Class": 2,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([76.94673041013195, 11.002409545496054]),
            {
              "Class": 2,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([76.94546406413848, 10.99020963771661]),
            {
              "Class": 2,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([76.97217667981991, 10.991210990056958]),
            {
              "Class": 2,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([77.07941866048424, 10.99321042858982]),
            {
              "Class": 2,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([77.20197668425216, 11.074546696035407]),
            {
              "Class": 2,
              "system:index": "26"
            }),
        ee.Feature(
            ee.Geometry.Point([77.20132460489108, 11.086703493504293]),
            {
              "Class": 2,
              "system:index": "27"
            }),
        ee.Feature(
            ee.Geometry.Point([77.1586450718429, 10.479562618794148]),
            {
              "Class": 2,
              "system:index": "28"
            }),
        ee.Feature(
            ee.Geometry.Point([77.97401512725796, 9.552234710936649]),
            {
              "Class": 2,
              "system:index": "29"
            }),
        ee.Feature(
            ee.Geometry.Point([78.09903413350463, 9.866375273486051]),
            {
              "Class": 2,
              "system:index": "30"
            }),
        ee.Feature(
            ee.Geometry.Point([77.23845318818306, 8.311979616104743]),
            {
              "Class": 2,
              "system:index": "31"
            }),
        ee.Feature(
            ee.Geometry.Point([77.24946646666221, 8.318065925709256]),
            {
              "Class": 2,
              "system:index": "32"
            }),
        ee.Feature(
            ee.Geometry.Point([77.18605966940189, 8.305595752038647]),
            {
              "Class": 2,
              "system:index": "33"
            }),
        ee.Feature(
            ee.Geometry.Point([77.97455988252929, 10.36503098763221]),
            {
              "Class": 2,
              "system:index": "34"
            }),
        ee.Feature(
            ee.Geometry.Point([77.97463632548622, 10.364852892929676]),
            {
              "Class": 2,
              "system:index": "35"
            }),
        ee.Feature(
            ee.Geometry.Point([78.8345357032384, 9.247931663778083]),
            {
              "Class": 2,
              "system:index": "36"
            }),
        ee.Feature(
            ee.Geometry.Point([79.76187310208957, 11.373043188084546]),
            {
              "Class": 2,
              "system:index": "37"
            }),
        ee.Feature(
            ee.Geometry.Point([79.79286466072257, 11.368097502376639]),
            {
              "Class": 2,
              "system:index": "38"
            }),
        ee.Feature(
            ee.Geometry.Point([79.73203160052148, 11.363431097375782]),
            {
              "Class": 2,
              "system:index": "39"
            }),
        ee.Feature(
            ee.Geometry.Point([79.72627206356051, 11.36114269727466]),
            {
              "Class": 2,
              "system:index": "40"
            }),
        ee.Feature(
            ee.Geometry.Point([79.69503639045828, 11.378999939021714]),
            {
              "Class": 2,
              "system:index": "41"
            }),
        ee.Feature(
            ee.Geometry.Point([77.35527911418478, 8.361896001511175]),
            {
              "Class": 2,
              "system:index": "42"
            }),
        ee.Feature(
            ee.Geometry.Point([77.3294539845153, 8.446762359874157]),
            {
              "Class": 2,
              "system:index": "43"
            }),
        ee.Feature(
            ee.Geometry.Point([77.32648699404783, 8.45174597924252]),
            {
              "Class": 2,
              "system:index": "44"
            }),
        ee.Feature(
            ee.Geometry.Point([77.39005575524475, 8.50122650084138]),
            {
              "Class": 2,
              "system:index": "45"
            }),
        ee.Feature(
            ee.Geometry.Point([77.2229766245114, 8.400384982966393]),
            {
              "Class": 2,
              "system:index": "46"
            }),
        ee.Feature(
            ee.Geometry.Point([77.30299968661151, 8.440508319698347]),
            {
              "Class": 2,
              "system:index": "47"
            }),
        ee.Feature(
            ee.Geometry.Point([77.30101657406726, 8.44041268357654]),
            {
              "Class": 2,
              "system:index": "48"
            }),
        ee.Feature(
            ee.Geometry.Point([77.30374835598681, 8.443941595390594]),
            {
              "Class": 2,
              "system:index": "49"
            }),
        ee.Feature(
            ee.Geometry.Point([77.6019532618833, 10.044822048834726]),
            {
              "Class": 2,
              "system:index": "50"
            }),
        ee.Feature(
            ee.Geometry.Point([77.59332140978604, 10.060772907333357]),
            {
              "Class": 2,
              "system:index": "51"
            }),
        ee.Feature(
            ee.Geometry.Point([77.47565941757902, 10.031206657060483]),
            {
              "Class": 2,
              "system:index": "52"
            }),
        ee.Feature(
            ee.Geometry.Point([77.47541028216892, 10.023361603730518]),
            {
              "Class": 2,
              "system:index": "53"
            }),
        ee.Feature(
            ee.Geometry.Point([77.45627045219747, 10.01156922151563]),
            {
              "Class": 2,
              "system:index": "54"
            }),
        ee.Feature(
            ee.Geometry.Point([80.25297995436898, 12.984075748118]),
            {
              "Class": 2,
              "system:index": "55"
            })])
    Built_Up = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([80.2007828524345, 12.986370718998982]),
            {
              "Class": 3,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([80.1633742083861, 13.224847249211951]),
            {
              "Class": 3,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([80.17221476929919, 13.21540541471174]),
            {
              "Class": 3,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([80.16829380692045, 13.230912734243487]),
            {
              "Class": 3,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([80.17189787883436, 13.230961989696521]),
            {
              "Class": 3,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([80.16289829347463, 13.23157527215365]),
            {
              "Class": 3,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([80.12260768924364, 13.200177509139944]),
            {
              "Class": 3,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([80.09681678276569, 13.167137243461918]),
            {
              "Class": 3,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([80.09354527936274, 13.167304747495434]),
            {
              "Class": 3,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([80.0458873189393, 13.179980941672579]),
            {
              "Class": 3,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([80.04444192115763, 13.170193495303463]),
            {
              "Class": 3,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([80.07696213069472, 13.134255656515343]),
            {
              "Class": 3,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([80.03503415860864, 13.145754171007091]),
            {
              "Class": 3,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([80.00512514451006, 13.150796186096903]),
            {
              "Class": 3,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([80.00346204179827, 13.150601410921055]),
            {
              "Class": 3,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([79.47864364840542, 13.314737579779715]),
            {
              "Class": 3,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([79.43589333301149, 13.27397941251243]),
            {
              "Class": 3,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([79.51889988156957, 13.144920698824043]),
            {
              "Class": 3,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([79.50769935076207, 13.135259257382206]),
            {
              "Class": 3,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([79.44288128427061, 13.103161454538139]),
            {
              "Class": 3,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([79.67855679647397, 13.02445362667772]),
            {
              "Class": 3,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([79.63889350987911, 12.997137506162309]),
            {
              "Class": 3,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([79.55591972398925, 12.950432275239388]),
            {
              "Class": 3,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([79.55144262634734, 12.941889973334792]),
            {
              "Class": 3,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([79.54266384988829, 12.913450702320024]),
            {
              "Class": 3,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([79.54367537218641, 12.914454220493788]),
            {
              "Class": 3,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([76.86329656735262, 11.046228110067492]),
            {
              "Class": 3,
              "system:index": "26"
            }),
        ee.Feature(
            ee.Geometry.Point([76.86554191226881, 11.037266446823244]),
            {
              "Class": 3,
              "system:index": "27"
            }),
        ee.Feature(
            ee.Geometry.Point([76.94332554092026, 10.998815909016434]),
            {
              "Class": 3,
              "system:index": "28"
            }),
        ee.Feature(
            ee.Geometry.Point([76.94587970330217, 10.9977038233877]),
            {
              "Class": 3,
              "system:index": "29"
            }),
        ee.Feature(
            ee.Geometry.Point([76.95517488444763, 10.993397484255405]),
            {
              "Class": 3,
              "system:index": "30"
            }),
        ee.Feature(
            ee.Geometry.Point([77.12425639353718, 10.566657448905985]),
            {
              "Class": 3,
              "system:index": "31"
            }),
        ee.Feature(
            ee.Geometry.Point([77.01178028674609, 10.661026737605015]),
            {
              "Class": 3,
              "system:index": "32"
            }),
        ee.Feature(
            ee.Geometry.Point([77.05782556016281, 10.939861236506852]),
            {
              "Class": 3,
              "system:index": "33"
            }),
        ee.Feature(
            ee.Geometry.Point([78.14007616782077, 11.060137890526182]),
            {
              "Class": 3,
              "system:index": "34"
            }),
        ee.Feature(
            ee.Geometry.Point([76.98011343691641, 10.53811132017623]),
            {
              "Class": 3,
              "system:index": "35"
            }),
        ee.Feature(
            ee.Geometry.Point([77.38345829251833, 9.84065470913113]),
            {
              "Class": 3,
              "system:index": "36"
            }),
        ee.Feature(
            ee.Geometry.Point([78.11250412640152, 10.104874475942546]),
            {
              "Class": 3,
              "system:index": "37"
            }),
        ee.Feature(
            ee.Geometry.Point([77.247256884176, 9.682157771115687]),
            {
              "Class": 3,
              "system:index": "38"
            }),
        ee.Feature(
            ee.Geometry.Point([77.50397686638988, 9.81057898876076]),
            {
              "Class": 3,
              "system:index": "39"
            }),
        ee.Feature(
            ee.Geometry.Point([77.4915096209043, 9.97009098909339]),
            {
              "Class": 3,
              "system:index": "40"
            }),
        ee.Feature(
            ee.Geometry.Point([77.43395722006949, 8.172206744903013]),
            {
              "Class": 3,
              "system:index": "41"
            }),
        ee.Feature(
            ee.Geometry.Point([77.29503246768012, 8.196253281692496]),
            {
              "Class": 3,
              "system:index": "42"
            }),
        ee.Feature(
            ee.Geometry.Point([77.26219041765304, 8.210263727200644]),
            {
              "Class": 3,
              "system:index": "43"
            }),
        ee.Feature(
            ee.Geometry.Point([77.28073863855, 8.293112405931314]),
            {
              "Class": 3,
              "system:index": "44"
            }),
        ee.Feature(
            ee.Geometry.Point([77.82828259934116, 8.25709274102186]),
            {
              "Class": 3,
              "system:index": "45"
            }),
        ee.Feature(
            ee.Geometry.Point([77.82875980527625, 8.265746880821]),
            {
              "Class": 3,
              "system:index": "46"
            }),
        ee.Feature(
            ee.Geometry.Point([77.88861512166547, 8.276164239168315]),
            {
              "Class": 3,
              "system:index": "47"
            }),
        ee.Feature(
            ee.Geometry.Point([77.89382393638762, 8.28092306854471]),
            {
              "Class": 3,
              "system:index": "48"
            }),
        ee.Feature(
            ee.Geometry.Point([77.91107622217619, 8.296980737533149]),
            {
              "Class": 3,
              "system:index": "49"
            }),
        ee.Feature(
            ee.Geometry.Point([78.22235180983117, 10.581273376418379]),
            {
              "Class": 3,
              "system:index": "50"
            }),
        ee.Feature(
            ee.Geometry.Point([77.97257202617833, 10.367686240813601]),
            {
              "Class": 3,
              "system:index": "51"
            }),
        ee.Feature(
            ee.Geometry.Point([79.69629518162733, 11.385683243252886]),
            {
              "Class": 3,
              "system:index": "52"
            }),
        ee.Feature(
            ee.Geometry.Point([79.68174260821966, 11.421864956420738]),
            {
              "Class": 3,
              "system:index": "53"
            }),
        ee.Feature(
            ee.Geometry.Point([79.79212206354615, 11.130119445733067]),
            {
              "Class": 3,
              "system:index": "54"
            }),
        ee.Feature(
            ee.Geometry.Point([79.80514926661733, 11.074922155859287]),
            {
              "Class": 3,
              "system:index": "55"
            }),
        ee.Feature(
            ee.Geometry.Point([77.21879127434651, 8.399297275840672]),
            {
              "Class": 3,
              "system:index": "56"
            }),
        ee.Feature(
            ee.Geometry.Point([77.31134771648136, 8.440736281046362]),
            {
              "Class": 3,
              "system:index": "57"
            }),
        ee.Feature(
            ee.Geometry.Point([77.31006709344899, 8.437211589937743]),
            {
              "Class": 3,
              "system:index": "58"
            }),
        ee.Feature(
            ee.Geometry.Point([77.4116677278787, 8.398442166536258]),
            {
              "Class": 3,
              "system:index": "59"
            }),
        ee.Feature(
            ee.Geometry.Point([77.44183169787578, 8.273463128302632]),
            {
              "Class": 3,
              "system:index": "60"
            }),
        ee.Feature(
            ee.Geometry.Point([77.43747823244048, 8.273775611875655]),
            {
              "Class": 3,
              "system:index": "61"
            }),
        ee.Feature(
            ee.Geometry.Point([80.216855750985, 12.980717173083374]),
            {
              "Class": 3,
              "system:index": "62"
            }),
        ee.Feature(
            ee.Geometry.Point([80.25847246136871, 12.999203162589481]),
            {
              "Class": 3,
              "system:index": "63"
            })])
    Vegetation = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([80.22538678862152, 13.000600417222593]),
            {
              "Class": 4,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([80.23220639292255, 13.018437638505494]),
            {
              "Class": 4,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([80.2693587099075, 13.125157701134116]),
            {
              "Class": 4,
              "system:index": "2"
            }),
        ee.Feature(
            ee.Geometry.Point([80.29646854542939, 13.187774115689468]),
            {
              "Class": 4,
              "system:index": "3"
            }),
        ee.Feature(
            ee.Geometry.Point([80.26682525483628, 13.212206941437303]),
            {
              "Class": 4,
              "system:index": "4"
            }),
        ee.Feature(
            ee.Geometry.Point([80.25545334401087, 13.216760851904935]),
            {
              "Class": 4,
              "system:index": "5"
            }),
        ee.Feature(
            ee.Geometry.Point([80.23685735975161, 13.227309800225662]),
            {
              "Class": 4,
              "system:index": "6"
            }),
        ee.Feature(
            ee.Geometry.Point([80.21720157371941, 13.222910111591984]),
            {
              "Class": 4,
              "system:index": "7"
            }),
        ee.Feature(
            ee.Geometry.Point([80.18453277195574, 13.232352183640206]),
            {
              "Class": 4,
              "system:index": "8"
            }),
        ee.Feature(
            ee.Geometry.Point([80.1729535046235, 13.232457803177063]),
            {
              "Class": 4,
              "system:index": "9"
            }),
        ee.Feature(
            ee.Geometry.Point([80.16032421361443, 13.237049822753825]),
            {
              "Class": 4,
              "system:index": "10"
            }),
        ee.Feature(
            ee.Geometry.Point([80.08365310711612, 13.174414135975665]),
            {
              "Class": 4,
              "system:index": "11"
            }),
        ee.Feature(
            ee.Geometry.Point([80.07847376150836, 13.17465832188996]),
            {
              "Class": 4,
              "system:index": "12"
            }),
        ee.Feature(
            ee.Geometry.Point([80.06850172358776, 13.176172427699415]),
            {
              "Class": 4,
              "system:index": "13"
            }),
        ee.Feature(
            ee.Geometry.Point([80.05067770601339, 13.180892926287479]),
            {
              "Class": 4,
              "system:index": "14"
            }),
        ee.Feature(
            ee.Geometry.Point([80.0448598070496, 13.181405204195457]),
            {
              "Class": 4,
              "system:index": "15"
            }),
        ee.Feature(
            ee.Geometry.Point([80.05887282266288, 13.136802799992092]),
            {
              "Class": 4,
              "system:index": "16"
            }),
        ee.Feature(
            ee.Geometry.Point([80.01508317823036, 13.151916699710876]),
            {
              "Class": 4,
              "system:index": "17"
            }),
        ee.Feature(
            ee.Geometry.Point([79.89014292908443, 13.137287029074527]),
            {
              "Class": 4,
              "system:index": "18"
            }),
        ee.Feature(
            ee.Geometry.Point([79.41950554467819, 13.254157472811375]),
            {
              "Class": 4,
              "system:index": "19"
            }),
        ee.Feature(
            ee.Geometry.Point([79.47524900677503, 13.163299433144603]),
            {
              "Class": 4,
              "system:index": "20"
            }),
        ee.Feature(
            ee.Geometry.Point([79.47847641791341, 13.150104739654111]),
            {
              "Class": 4,
              "system:index": "21"
            }),
        ee.Feature(
            ee.Geometry.Point([79.489810001355, 13.121322833078269]),
            {
              "Class": 4,
              "system:index": "22"
            }),
        ee.Feature(
            ee.Geometry.Point([79.45939040335129, 13.103714733880885]),
            {
              "Class": 4,
              "system:index": "23"
            }),
        ee.Feature(
            ee.Geometry.Point([79.63642143925162, 12.993059724761332]),
            {
              "Class": 4,
              "system:index": "24"
            }),
        ee.Feature(
            ee.Geometry.Point([79.59738305134687, 12.967726232432364]),
            {
              "Class": 4,
              "system:index": "25"
            }),
        ee.Feature(
            ee.Geometry.Point([76.86827369264988, 11.037968959631659]),
            {
              "Class": 4,
              "system:index": "26"
            }),
        ee.Feature(
            ee.Geometry.Point([76.87016871358381, 11.034702666818383]),
            {
              "Class": 4,
              "system:index": "27"
            }),
        ee.Feature(
            ee.Geometry.Point([76.88364955873575, 11.01983400427607]),
            {
              "Class": 4,
              "system:index": "28"
            }),
        ee.Feature(
            ee.Geometry.Point([76.98497978624296, 11.001072347964849]),
            {
              "Class": 4,
              "system:index": "29"
            }),
        ee.Feature(
            ee.Geometry.Point([77.1377293223433, 10.575145076531555]),
            {
              "Class": 4,
              "system:index": "30"
            }),
        ee.Feature(
            ee.Geometry.Point([77.09459257070176, 10.718076144652397]),
            {
              "Class": 4,
              "system:index": "31"
            }),
        ee.Feature(
            ee.Geometry.Point([78.22439753815458, 10.969847278753846]),
            {
              "Class": 4,
              "system:index": "32"
            }),
        ee.Feature(
            ee.Geometry.Point([77.36818960547062, 9.819265021366935]),
            {
              "Class": 4,
              "system:index": "33"
            }),
        ee.Feature(
            ee.Geometry.Point([77.50362922417611, 9.836890750085608]),
            {
              "Class": 4,
              "system:index": "34"
            }),
        ee.Feature(
            ee.Geometry.Point([77.50210077376072, 9.875770029780234]),
            {
              "Class": 4,
              "system:index": "35"
            }),
        ee.Feature(
            ee.Geometry.Point([77.49987656196225, 9.978795302220819]),
            {
              "Class": 4,
              "system:index": "36"
            }),
        ee.Feature(
            ee.Geometry.Point([77.42400138492292, 8.174515383146439]),
            {
              "Class": 4,
              "system:index": "37"
            }),
        ee.Feature(
            ee.Geometry.Point([77.39902451647175, 8.18353132105574]),
            {
              "Class": 4,
              "system:index": "38"
            }),
        ee.Feature(
            ee.Geometry.Point([77.32218775678719, 8.199159047831795]),
            {
              "Class": 4,
              "system:index": "39"
            }),
        ee.Feature(
            ee.Geometry.Point([77.29650874189943, 8.196324807805121]),
            {
              "Class": 4,
              "system:index": "40"
            }),
        ee.Feature(
            ee.Geometry.Point([77.27115572014424, 8.301921575263394]),
            {
              "Class": 4,
              "system:index": "41"
            }),
        ee.Feature(
            ee.Geometry.Point([77.82556801668558, 8.249251569092538]),
            {
              "Class": 4,
              "system:index": "42"
            }),
        ee.Feature(
            ee.Geometry.Point([77.82776041807242, 8.249779312213425]),
            {
              "Class": 4,
              "system:index": "43"
            }),
        ee.Feature(
            ee.Geometry.Point([77.9159679765374, 8.295762934025126]),
            {
              "Class": 4,
              "system:index": "44"
            }),
        ee.Feature(
            ee.Geometry.Point([77.93982069096467, 8.30804916061538]),
            {
              "Class": 4,
              "system:index": "45"
            }),
        ee.Feature(
            ee.Geometry.Point([78.0349614091402, 8.368932555444426]),
            {
              "Class": 4,
              "system:index": "46"
            }),
        ee.Feature(
            ee.Geometry.Point([78.1228670958133, 10.581470519462798]),
            {
              "Class": 4,
              "system:index": "47"
            }),
        ee.Feature(
            ee.Geometry.Point([79.62376068486958, 11.43254218002367]),
            {
              "Class": 4,
              "system:index": "48"
            }),
        ee.Feature(
            ee.Geometry.Point([79.68401323369378, 11.444397685358782]),
            {
              "Class": 4,
              "system:index": "49"
            }),
        ee.Feature(
            ee.Geometry.Point([79.75494356537881, 11.128951433236757]),
            {
              "Class": 4,
              "system:index": "50"
            }),
        ee.Feature(
            ee.Geometry.Point([79.76174710149246, 11.127998513856971]),
            {
              "Class": 4,
              "system:index": "51"
            }),
        ee.Feature(
            ee.Geometry.Point([77.30896604664838, 8.43695157819716]),
            {
              "Class": 4,
              "system:index": "52"
            }),
        ee.Feature(
            ee.Geometry.Point([77.31251587805444, 8.437737970340269]),
            {
              "Class": 4,
              "system:index": "53"
            }),
        ee.Feature(
            ee.Geometry.Point([77.32058072546337, 8.449620231997553]),
            {
              "Class": 4,
              "system:index": "54"
            }),
        ee.Feature(
            ee.Geometry.Point([77.2987173884795, 8.451634901609806]),
            {
              "Class": 4,
              "system:index": "55"
            }),
        ee.Feature(
            ee.Geometry.Point([77.41966179373269, 8.398126925272713]),
            {
              "Class": 4,
              "system:index": "56"
            }),
        ee.Feature(
            ee.Geometry.Point([77.41638881243018, 8.397434807037804]),
            {
              "Class": 4,
              "system:index": "57"
            }),
        ee.Feature(
            ee.Geometry.Point([80.26458384329723, 12.991524221657716]),
            {
              "Class": 4,
              "system:index": "58"
            }),
        ee.Feature(
            ee.Geometry.Point([80.25256878318471, 12.998645630592486]),
            {
              "Class": 4,
              "system:index": "59"
            })])
    #imageVisParam = {"opacity":1,"bands":["B4","B3","B2"],"min":1927.8285714285714,"max":2870.4571428571426,"gamma":1}
    FallowLand = ee.FeatureCollection(
        [ee.Feature(
            ee.Geometry.Point([80.13589957460904, 13.162341530650133]),
            {
              "Class": 5,
              "system:index": "0"
            }),
        ee.Feature(
            ee.Geometry.Point([80.23425285556134, 13.22537139866226]),
            {
              "Class": 5,
              "system:index": "1"
            }),
        ee.Feature(
            ee.Geometry.Point([79.5550855079372, 12.951400060058107]),
            {
              "Class": 5,
              "system:index": "2"
            })])
    #imageVisParam = {'bands': ['B4', 'B3', 'B2'], 'gamma': 1.0, 'min': 371.3571428571428, 'max': 2910.214285714286}
    imageVisParam = {"opacity":1,"bands":["B4","B3","B2"],"min":208.47,"max":1719.03,"gamma":1} #updated
#***************************************************************************************************************************************
    points = Water_Bodies.merge(Vegetation).merge(Built_Up).merge(Sand).merge(FallowLand)

# Sample the image at the points (extract features for classification)
    training = image.sampleRegions(
    collection=points,  # Pass 'points' as the first positional argument
    properties=['Class'],
    scale=10
)

# Train a classifier (e.g., Random Forest)
    classifier = ee.Classifier.smileRandomForest(100).train(
    #training,  # Pass training as the first positional argument
    #'Class',    # Pass 'class' as the second positional argument (classProperty)
    #bands.bandNames()  # Pass bands.bandNames() as the third positional argument (inputProperties)
    features=training, 
    classProperty='Class', 
    inputProperties=bands.bandNames()
)

# Classify the image using the trained classifier
    classified = image.classify(classifier)

    centroid = roi.centroid().coordinates().getInfo()
    lon, lat = centroid
    Map = geemap.Map(center=[lat, lon], zoom=10)

    imageVisParam = {'bands': ['B4', 'B3', 'B2'], 'gamma': 1.0, 'min': 371.3571428571428, 'max': 2910.214285714286}
    ndvi_vis = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
    classified_vis = {'min': 1, 'max': 5, 'palette': ['yellow', 'blue', 'red', 'green', 'orange']}

    Map.addLayer(roi, {'color': 'red', 'opacity': 0.5}, 'Boundary')
    Map.addLayer(classified, classified_vis, 'LULC Classification')
    Map.addLayer(image, imageVisParam, "Satellite Imagery")
    Map.addLayer(ndvi, ndvi_vis, 'NDVI')

    add_ui_elements(Map)

def add_ui_elements(map_object):
    legend_html = """
    <div style="position: fixed; bottom: 60px; left: 48px; width: 180px;
                background-color: white; z-index:9999; font-size:14px;
                padding: 10px; border-radius: 5px; border: 1px solid black;">
    <b>Legend</b><br>
    <i style="background:blue;width:15px;height:15px;display:inline-block;margin-right:5px;"></i> Water<br>
    <i style="background:green;width:15px;height:15px;display:inline-block;margin-right:5px;"></i> Vegetation<br>
    <i style="background:red;width:15px;height:15px;display:inline-block;margin-right:5px;"></i> Urban<br>
    <i style="background:yellow;width:15px;height:15px;display:inline-block;margin-right:5px;"></i> Sand<br>
    <i style="background:orange;width:15px;height:15px;display:inline-block;margin-right:5px;"></i> Fallow<br>
    </div>
    """
    button_html = """
    <div style="position: fixed; bottom: 10px; right: 10px; z-index: 1000;">
        <button onclick="export_layers()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
            Export Data
        </button>
    </div>
    <script>
        function export_layers() {
            alert('Exporting and downloading NDVI, LULC, and Satellite imagery...');
            fetch('/export_layers', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => { alert(data.message); })
            .catch(error => { alert('Export failed: ' + error); });
        }
    </script>
    """
    map_object.get_root().html.add_child(folium.Element(legend_html + button_html))

def download_from_drive(filename_prefix, gauth):
    drive = GoogleDrive(gauth)
    query = f"title contains '{filename_prefix}' and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()

    if not file_list:
        print(f"❌ File not found: {filename_prefix}")
        return

    for file in file_list:
        file.FetchMetadata(fields='title, fileSize, downloadUrl')
        download_url = file['downloadUrl']
        file_size = int(file['fileSize'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{file['title'].replace('.tif', '')}_{timestamp}.tif"

        print(f"⬇️ Downloading {new_filename} ({file_size / 1e6:.2f} MB)...")
        access_token = gauth.credentials.access_token
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(download_url, headers=headers, stream=True)
        with open(new_filename, 'wb') as f, tqdm(
            desc=new_filename,
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        print(f"✅ Downloaded: {new_filename}")

def export_layers_task():
    try:
        print("📤 Starting export tasks...")

        tasks = {
            'NDVI_output': ee.batch.Export.image.toDrive(
                image=ndvi, description='Export_NDVI',
                fileNamePrefix='NDVI_output', scale=10,
                region=roi, fileFormat='GeoTIFF'
            ),
            'LULC_output': ee.batch.Export.image.toDrive(
                image=classified, description='Export_Classified',
                fileNamePrefix='LULC_output', scale=10,
                region=roi, fileFormat='GeoTIFF'
            ),
            'Satellite_output': ee.batch.Export.image.toDrive(
                image=image, description='Export_Satellite',
                fileNamePrefix='Satellite_output', scale=10,
                region=roi, fileFormat='GeoTIFF'
            )
        }

        for task in tasks.values():
            task.start()

        print("⏳ Waiting for tasks to finish...")
        while any(t.active() for t in tasks.values()):
            time.sleep(30)
            for name, t in tasks.items():
                print(f"🔄 {name}: {t.status()['state']}")

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

#***************************************************************************************************************************
# Tell PyDrive to look for client_secrets.json here
        gauth.LoadClientConfigFile("D:/INTERNSHIP_MSSRF_2025/Satellite_data/Final_python/client_secrets.json")

# Load previously saved credentials, if available
        gauth.LoadCredentialsFile("my_credentials.json")

# If no saved creds, authenticate manually (once)
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

# Save creds for future runs
        gauth.SaveCredentialsFile("my_credentials.json")
#***************************************************************************************************************************

        for prefix, task in tasks.items():
            if task.status()['state'] == 'COMPLETED':
                download_from_drive(prefix, gauth)
            else:
                print(f"❌ Task {prefix} failed or incomplete.")

    except Exception as e:
        print(f"❌ Error during export/download: {e}")

@app.route('/')
def index():
    process_layers()
    upload_form = '''
        <form action="/upload_shapefile" method="post" enctype="multipart/form-data" style="margin: 20px;">
            <label>Select a zipped shapefile:</label>
            <input type="file" name="shapefile_zip">
            <input type="submit" value="Upload">
        </form>
    '''
    return upload_form + Map.to_html()

@app.route('/upload_shapefile', methods=['POST'])
def upload_shapefile():
    file = request.files.get('shapefile_zip')
    if not file:
        return "No file uploaded", 400

    upload_folder = "uploaded_shapefiles"
    os.makedirs(upload_folder, exist_ok=True)
    zip_path = os.path.join(upload_folder, file.filename)
    file.save(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(upload_folder)

    shp_file = None
    for fname in os.listdir(upload_folder):
        if fname.endswith('.shp'):
            shp_file = os.path.join(upload_folder, fname)
            break

    if not shp_file:
        return "Shapefile (.shp) not found", 400

    gdf = gpd.read_file(shp_file)
    try:
        global roi
        ee_roi = geemap.geopandas_to_ee(gdf)
        roi = ee_roi.geometry()
        #process_layers()  # Reprocess using new ROI
        shutil.rmtree(upload_folder)
    except Exception as e:
        return f"Error converting to Earth Engine geometry: {str(e)}", 500

    return '''
    <script>
        alert("Shapefile uploaded successfully! Reloading map...");
        window.location.href = "/";
    </script>
    '''


@app.route('/export_layers', methods=['POST'])
def export_layers():
    threading.Thread(target=export_layers_task).start()
    return jsonify({'message': 'Exporting and downloading in background. Please check console logs for progress.'})

if __name__ == '__main__':
    process_layers()
    threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.2:5004")).start()
    serve(app, host='127.0.0.2', port=5004)
