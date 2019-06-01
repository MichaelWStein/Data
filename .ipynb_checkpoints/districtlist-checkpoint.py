import urllib.request
import json
import pandas as pd

def getdata(url):

    data = urllib.request.urlopen(url).read()
    data1 = data[2:]
    output = json.loads(data1)

    return output

url = "https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=FED&cpt=35"
distlist = []

for data in getdata(url)['DATA'] :
    distlist.append(data[0])

for data in distlist:
    print (f'https://www12.statcan.gc.ca/rest/census-recensement/CPR2016.json?lang=E&dguid={data}&topic=10&theme=5&notes=0')
