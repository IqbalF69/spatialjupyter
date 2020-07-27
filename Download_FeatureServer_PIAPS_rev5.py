import urllib.request, os
import json
import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()
# Variables
layerName = "PIAPS_V"
nameListFID = layerName+ ".json"
FolderJsons = "Output_"+ layerName
ID = "FID" #FID or OBJECTID

myUrl = "https://geoportal.menlhk.go.id/arcgis/rest/services/KLHK"
myService = "/"+layerName+"/MapServer/0/"

multiplier1st = 1000
print("initiating multiplier " + str(multiplier1st))


myParams = "query?where="+ID+">-2&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&f=pjson"

# Query ArcGIS Server Map Service
myRequest = myUrl + myService + myParams
#r = http.request('GET', myRequest)
response = urllib.request.urlopen(myRequest,context=context)
#myJSON = json.loads(r.data.decode('utf-8'))
myJSON = response.read()

# Write response to json text file

foo = open(nameListFID, "wb")
foo.write(myJSON);
foo.close()
'''
with open(nameListFID, 'w') as json_file:
  json.dump(myJSON, json_file)
'''
current_directory = os.getcwd()
final_directory = os.path.join(current_directory,FolderJsons)
if not os.path.exists(final_directory):
    os.makedirs(final_directory)

json_data = open(nameListFID, "r").read()
data = json.loads(json_data)
listD = data['objectIds']
lenD = max(listD)
print("Calculating maximum object id: " + str(lenD))

divMult1 = int(lenD / multiplier1st) #1000
modMult1 = int(lenD % multiplier1st)
if modMult1 != 0:
    divMult1 += 1

def multiplier2nd(maxb, divider):
    a = []
    multiplier = int(multiplier1st/divider)
    divMult2 = int(maxb / multiplier)
    modMult2 = int(maxb % multiplier)
    if modMult2 != 0:
        divMult2 += 1
    a.append(multiplier)
    a.append(divMult2)
    a.append(modMult2)
    return a

def readWebgis(a,b):
    print ("Processing FID: [" + a + ","+ b + "]")
    ParamText1 = "query?where="+ID+"+>%3D+"          #CHANGE
    ParamTextAnd = "+AND+"+ID+"+<"
    ParamText3 = "&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&returnZ=false&returnM=false&returnDistinctValues=false&returnTrueCurves=false&f=pjson"
    iterRequest = myUrl + myService + ParamText1 + a + ParamTextAnd + b + ParamText3
    print("reading URL WEBGIS: " + iterRequest)
    response = urllib.request.urlopen(iterRequest,context=context)
    #r = http.request('GET', myRequest)
    print("URL opened!")
    print ("Reading JSON files: [" + a + ","+ b + "]")
    #myJSON = json.loads(r.data.decode('utf-8'))
    myJSON = response.read()
    dirF = os.path.join(final_directory,"jsonOutput"+b+".json")
    # Write response to json text file
    foo = open(dirF, "wb")
    foo.write(myJSON);
    foo.close()
    '''
    with open(nameListFID, 'w') as json_file:
        json.dump(myJSON, json_file)
    '''
    global fileSize
    fileSize = os.stat(dirF).st_size
    print ("checking file size [" + a + ","+ b + "], (error 500 indicator: if Filesize < 1kb)")
    return dirF
listErrA = []
listErrB = []

for i in range(divMult1): #1000
    #if i < 98:
     #   continue
    a = str(i*multiplier1st)
    if i*multiplier1st + multiplier1st <= lenD:
        b = str(i*multiplier1st + multiplier1st)
    else:
        b = str(i*multiplier1st + modMult1)
    readWebgis(a,b)
    if fileSize < 100:
        listErrA.append(int(a))
        listErrB.append(int(b))
        print ("Error found in : [" + a + ","+ b + "] \n--------appending to list A and B")
    #if i < lenD:
    #    break
print(listErrA)
print(listErrB)
listErr2A = []      #500 * 2 = 1000
listErr2B = []
def Loopmultiplier(listErrA, listErrB, divider, listErr2A,listErr2B):
    for i in range(len(listErrA)):
        a = listErrA[i]
        maxb = listErrB[i]
        multiplier2nd(maxb, divider)
        multiplier = multiplier2nd(maxb,divider)[0]
        divMult = multiplier2nd(maxb,divider)[1]
        modMult = multiplier2nd(maxb,divider)[2]
        print("trying multiplier :" +str(multiplier) )
        for i in range(divMult):
            if i*multiplier < a:
                continue
            A = str(i*multiplier)
            if i*multiplier+multiplier <= maxb:
                B = str(i*multiplier + multiplier)
            else:
                B = str(i*multiplier + modMult)
            readWebgis(A,B)
            if fileSize < 100:
                listErr2A.append(int(A))
                listErr2B.append(int(B))
                print ("Error found in : [" + A + ","+ B + "] \n--------appending to list A and B")
        print ("Processed JSON file " + str(i+1) + " of " + str(divMult) + "in multiplier : "+ str(multiplier) + "\n---------------")
    print(listErr2A)
    print(listErr2B)

'''
# Create Feature Class
ws = os.getcwd() + os.sep
arcpy.JSONToFeatures_conversion("jsonOutput.json", ws + "finalShapfile.shp")
'''
Loopmultiplier(listErrA, listErrB, 2, listErr2A,listErr2B)
listErr3A = []      #250 * 4 = 1000
listErr3B = []
Loopmultiplier(listErr2A, listErr2B, 4, listErr3A,listErr3B)
listErr4A = []      #125 * 8 = 1000
listErr4B = []
Loopmultiplier(listErr3A, listErr3B, 8, listErr4A,listErr4B)
listErr5A = []      #25 * 40 = 1000
listErr5B = []
Loopmultiplier(listErr4A, listErr4B, 40, listErr5A,listErr5B)
listErr6A = []      #5 * 200 = 1000
listErr6B = []
Loopmultiplier(listErr5A, listErr5B, 200, listErr6A,listErr6B)
listErr7A = []      #1 * 1000 = 1000
listErr7B = []
Loopmultiplier(listErr6A, listErr6B, 200, listErr7A,listErr7B)
