import urllib.request
import json
import pandas as pd

#need to make sure that the correct program for province and district is run - right now just change code
def getdata(url):

    data = urllib.request.urlopen(url).read()
    data1 = data[2:]
    output = json.loads(data1)

    return output

url = "https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=FED&cpt=00"
distlist = []

for data in getdata(url)['DATA'] :
    distlist.append(data[0])

print(distlist)

# Creating a list for Canada and all Provinces

#url = "https://www12.statcan.gc.ca/rest/census-recensement/CR2016Geo.json?lang=E&geos=PR&cpt=00"
#provlist = []

#for data in getdata(url)['DATA'] :
#    provlist.append(data[0])

#print(provlist)