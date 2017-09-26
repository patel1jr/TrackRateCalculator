from flask import Flask,render_template,request
from werkzeug import secure_filename
import io
import csv
import json
from Tkinter import *
import csv
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import datetime
				 
# Define vertices of polygon track1 (lat/lon) t1
v0 = [42.093272, -83.310257] 
v1 = [42.091137, -83.308547]
v2 = [42.086636, -83.318287]
v3 = [42.088865, -83.320945]
v4 = [42.091282, -83.315504]

# Define vertices of polygon track2 (lat/lon) t1
v5 = [42.086226, -83.316043]
v6 = [42.083574, -83.316148]
v7 = [42.081037, -83.315811]
v8 = [42.081085, -83.313017]
v9 = [42.086284, -83.313952]


# Define vertices of polygon track3 (lat/lon) t1
v10 = [42.087979, -83.313248]
v11 = [42.085349, -83.313232]
v12 = [42.085434, -83.311358]
v13 = [42.086983, -83.311721]
v14 = [42.087986, -83.311915]


# Define vertices of polygon track4 (lat/lon) t1
v15 = [42.084879, -83.311229]
v16 = [42.084895, -83.309215]
v17 = [42.081296, -83.309042]
v18 = [42.081352, -83.311047]
v19 = [42.083144, -83.311026]



# Define vertices of polygon parking1 (lat/lon) t2
v20 = [42.393905, -83.436339]
v21 = [42.392277, -83.436714]
v22 = [42.392275, -83.435624]
v23 = [42.393050, -83.435114]
v24 = [42.393959, -83.434420]

# Define vertices of polygon parking2 (lat/lon) t2
v25 = [42.392615, -83.437936]
v26 = [42.393843, -83.437218]
v27 = [42.394093, -83.438216]
v28 = [42.393484, -83.438633]
v29 = [42.392871, -83.438933]


# Define vertices of polygon track1 (lat/lon) t3
v30 = [48.722459, -94.614673]
v31 = [48.717086, -94.614594]
v32 = [48.717082, -94.614162]
v33 = [48.720071, -94.613985]
v34 = [48.722480, -94.613977]



# Define vertices of polygon track2 (lat/lon) t3

v35 = [48.715728, -94.611828]
v36 = [48.715827, -94.605832]
v37 = [48.716598, -94.605823]
v38 = [48.716527, -94.608843]
v39 = [48.716407, -94.611686]



track1Poly = [Polygon([v0, v1, v2,v3,v4]),Polygon([v5, v6, v7,v8,v9]),Polygon([v10, v11, v12,v13,v14]),Polygon([v15, v16, v17,v18,v19])]
track2Poly = [Polygon([v20, v21, v22,v23,v24]),Polygon([v25, v26, v27,v28,v29])]
track3Poly = [Polygon([v30, v31, v32,v33,v34]),Polygon([v35, v36, v37,v38,v39])]
#print track3Poly[0]
#Price per track. Each entry contains price for t1,t2,.. etc.
trackCostJson = [{'c1':{'t1':(5,10,15,20),'t2':(4,8),'t3':(14,18)},'c2':{'t1':(3,6,9,12),'t2':(2,4),'t3':(12,14)},'c3':{'t1':(6,12,18,24),'t2':(8,10),'t3':(18,24)}}]

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__)

def check_point(a,b,trackPoly):
	point = Point(a,b)
	print point
	if trackPoly.contains(point):
		print "point is inside"
		return True
	return False


def rateCalculation(oem,trackNo,totalTimeForTrack):
	total=0
	perSectionCostArray=[]
	ratePerTrack = {}
	
	print len(totalTimeForTrack)
	for i in range(len(totalTimeForTrack)):
		perSectionCost = (totalTimeForTrack[i] * trackCostJson[0][oem][trackNo][i]) /60
		perSectionCostArray.append(perSectionCost)
		total += perSectionCost
 
	ratePerTrack["individualTrackCost"] = perSectionCostArray
	ratePerTrack["totalCost"] = total
	return ratePerTrack	


def calculateDuration(time_list):
	total = 0
	time_list = [t for t in time_list if t!= (None,None)]
		#filter(None,time_list)
		#time_list = set(time_list)
	time_list = set(time_list)
	print time_list        
		#print initial_time
		#print final_time
	for i,(initial_time,final_time) in enumerate(time_list):
		init = datetime.datetime.strptime(initial_time,"%Y-%m-%dT%H:%M:%S")
		fin = datetime.datetime.strptime(final_time,"%Y-%m-%dT%H:%M:%S")
			#print init
			#print fin
		time_difference = fin - init
		seconds = time_difference.total_seconds()
			#days = time_difference.days
		total = total + seconds
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60
		
	
	return total
	  
def timeCalculationForTrack(coordinate_list,trackPathPoly):
	first_element_switch = False
	last_element_switch = False
	initial_time = None
	final_time = None
	
	durationPerPathArray = []
	#print trackPathPoly
	#print trackPathPoly[0]
	for j in range(len(trackPathPoly)):
		print "checking for path no "+ str(j)
		timestampList = []
		for i in range(0,len(coordinate_list)):
			x, y = coordinate_list[i][1],coordinate_list[i][2]
				
			if check_point(x,y,trackPathPoly[j]):
				#print str(Point(y,x)) + " is inside Path No" + i
				if first_element_switch == False:
					initial_time = coordinate_list[i][0]
					first_element_switch = True
					last_element_switch = True
													
				if last_element_switch == True:
					final_time = coordinate_list[i][0]
						
			else:
				first_element_switch = False
				t = (initial_time,final_time)
				timestampList.append(tuple(t))
		t1 = (initial_time,final_time)
		timestampList.append(tuple(t1))
		durationPerPathArray.append(calculateDuration(timestampList))

	print "duration path array :" + str(durationPerPathArray)	
	return durationPerPathArray

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def car_path():
	return render_template('index.html')

@app.route('/trackRate',methods=['POST','GET'])
def calculation():
	
	if request.method == 'POST':
		files = request.files['file']
		#files.save(secure_filename(files.filename))
		#stream = io.StringIO(files.stream.read().decode("UTF8"),newline=None)
		select = request.form.get('comp_select')
		print select
		oem = request.form.get('oem_select1')
		print oem
		if files and allowed_file(files.filename):

			#with open(files,'rb') as f:
			reader = csv.reader(files)
			coordinate_list = list(reader)
		
			for row in coordinate_list:
				for k in (1,2):
					row[k] = float(row[k])
			

			if (select == "t1"):
				DurationArrayForTrack = timeCalculationForTrack(coordinate_list,track1Poly)
				print track1Poly[0]
			elif(select == "t2"):
				DurationArrayForTrack = timeCalculationForTrack(coordinate_list,track2Poly)
				
			elif(select == "t3"):
				DurationArrayForTrack = timeCalculationForTrack(coordinate_list,track3Poly)
				
			else:
				print "Error"
			
			totalDurationForTrack = 0
			for i in range(0,len(DurationArrayForTrack)):
					totalDurationForTrack+=DurationArrayForTrack[i]

			amt = rateCalculation(oem,'t1',DurationArrayForTrack)
			print amt["individualTrackCost"]

			return render_template("trackRate.html",calculation=calculation,path_and_track_total = zip(DurationArrayForTrack,amt["individualTrackCost"]),final_total=totalDurationForTrack, final_amount = amt["totalCost"],site=select,company=oem)
	


if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
