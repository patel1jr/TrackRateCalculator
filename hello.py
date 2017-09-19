from flask import Flask,render_template,request
from werkzeug import secure_filename
import io
import csv

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
lats_vect = np.array([v0[0],v1[0],v2[0],v3[0],v4[0]])
lons_vect = np.array([v0[1],v1[1],v2[1],v3[1],v4[1]])

# Define vertices of polygon track2 (lat/lon) t1
v5 = [42.086226, -83.316043]
v6 = [42.083574, -83.316148]
v7 = [42.081037, -83.315811]
v8 = [42.081085, -83.313017]
v9 = [42.086284, -83.313952]
lats_vect2 = np.array([v5[0],v6[0],v7[0],v8[0],v9[0]])
lons_vect2 = np.array([v5[1],v6[1],v7[1],v8[1],v9[1]])

# Define vertices of polygon track3 (lat/lon) t1
v10 = [42.087979, -83.313248]
v11 = [42.085349, -83.313232]
v12 = [42.085434, -83.311358]
v13 = [42.086983, -83.311721]
v14 = [42.087986, -83.311915]
lats_vect3 = np.array([v10[0],v11[0],v12[0],v13[0],v14[0]])
lons_vect3 = np.array([v10[1],v11[1],v12[1],v13[1],v14[1]])

# Define vertices of polygon track4 (lat/lon) t1
v15 = [42.084879, -83.311229]
v16 = [42.084895, -83.309215]
v17 = [42.081296, -83.309042]
v18 = [42.081352, -83.311047]
v19 = [42.083144, -83.311026]
lats_vect4 = np.array([v15[0],v16[0],v17[0],v18[0],v19[0]])
lons_vect4 = np.array([v15[1],v16[1],v17[1],v18[1],v19[1]])


# Define vertices of polygon parking1 (lat/lon) t2
v20 = [42.393905, -83.436339]
v21 = [42.392277, -83.436714]
v22 = [42.392275, -83.435624]
v23 = [42.393050, -83.435114]
v24 = [42.393959, -83.434420]
lats_vect5 = np.array([v20[0],v21[0],v22[0],v23[0],v24[0]])
lons_vect5 = np.array([v20[1],v21[1],v22[1],v23[1],v24[1]])
# Define vertices of polygon parking2 (lat/lon) t2
v25 = [42.392615, -83.437936]
v26 = [42.393843, -83.437218]
v27 = [42.394093, -83.438216]
v28 = [42.393484, -83.438633]
v29 = [42.392871, -83.438933]
lats_vect6 = np.array([v25[0],v26[0],v27[0],v28[0],v29[0]])
lons_vect6 = np.array([v25[1],v26[1],v27[1],v28[1],v29[1]])

# Define vertices of polygon track1 (lat/lon) t3
v30 = [48.722459, -94.614673]
v31 = [48.717086, -94.614594]
v32 = [48.717082, -94.614162]
v33 = [48.720071, -94.613985]
v34 = [48.722480, -94.613977]
lats_vect7 = np.array([v30[0],v31[0],v32[0],v33[0],v34[0]])
lons_vect7 = np.array([v30[1],v31[1],v32[1],v33[1],v34[1]])


# Define vertices of polygon track2 (lat/lon) t3

v35 = [48.715728, -94.611828]
v36 = [48.715827, -94.605832]
v37 = [48.716598, -94.605823]
v38 = [48.716527, -94.608843]
v39 = [48.716407, -94.611686]
lats_vect8 = np.array([v35[0],v36[0],v37[0],v38[0],v39[0]])
lons_vect8 = np.array([v35[1],v36[1],v37[1],v38[1],v39[1]])

#Price per track. Each entry contains price for t1,t2,.. etc.
c1t1 = [5,10,15,20]
c2t1 = [3,6,9,12]
c3t1 = [6,12,18,24]

c1t2 = [4,8]
c2t2 = [2,4]
c3t2 = [8,10]

c1t3 = [14,18]
c2t3 = [12,14]
c3t3 = [18,24]







ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__)


def check_point(a,b,lons_vectx,lats_vectx):
	lons_lats_vect = np.column_stack((lons_vectx,lats_vectx)) #Reshape coordinates
	polygon = Polygon(lons_lats_vect) #create polygon
	point = Point(b,a)
	if polygon.contains(point):
		return True
	return False

def rate_calculation_t1(oem,path1_time,path2_time,path3_time,path4_time):
	if oem == "c1":
		track1_c1_amount = path1_time * c1t1[0] /60
		track2_c1_amount = path2_time * c1t1[1] /60
		track3_c1_amount = path3_time * c1t1[2] /60
		track4_c1_amount = path4_time * c1t1[3] /60

		
		c1_amount = [track1_c1_amount,track2_c1_amount,track3_c1_amount,track4_c1_amount]

		return c1_amount

	elif oem == "c2":
		track1_c2_amount = path1_time * c2t1[0] /60
		track2_c2_amount = path2_time * c2t1[1] /60
		track3_c2_amount = path3_time * c2t1[2] /60
		track4_c2_amount = path4_time * c2t1[3] /60

		
		c2_amount = [track1_c2_amount,track2_c2_amount,track3_c2_amount,track4_c2_amount]

		return c2_amount		

	elif oem == "c3":
		track1_c3_amount = path1_time * c3t1[0] /60
		track2_c3_amount = path2_time * c3t1[1] /60
		track3_c3_amount = path3_time * c3t1[2] /60
		track4_c3_amount = path4_time * c3t1[3] /60

		
		c3_amount = [track1_c3_amount,track2_c3_amount,track3_c3_amount,track4_c3_amount]

		return c3_amount

def rate_calculation_t2(oem,path1_time,path2_time):
	if oem == "c1":
		track1_c1_amount = path1_time * c1t2[0] /60
		track2_c1_amount = path2_time * c1t2[1] /60
		

		
		c1_amount = [track1_c1_amount,track2_c1_amount]

		return c1_amount

	elif oem == "c2":
		track1_c2_amount = path1_time * c2t2[0] /60
		track2_c2_amount = path2_time * c2t2[1] /60


		
		c2_amount = [track1_c2_amount,track2_c2_amount]

		return c2_amount		

	elif oem == "c3":
		track1_c3_amount = path1_time * c3t2[0] /60
		track2_c3_amount = path2_time * c3t2[1] /60


		
		c3_amount = [track1_c3_amount,track2_c3_amount]

		return c3_amount
def rate_calculation_t3(oem,path1_time,path2_time):
	if oem == "c1":
		track1_c1_amount = path1_time * c1t3[0] /60
		track2_c1_amount = path2_time * c1t3[1] /60
		

		
		c1_amount = [track1_c1_amount,track2_c1_amount]

		return c1_amount

	elif oem == "c2":
		track1_c2_amount = path1_time * c2t3[0] /60
		track2_c2_amount = path2_time * c2t3[1] /60


		
		c2_amount = [track1_c2_amount,track2_c2_amount]

		return c2_amount		

	elif oem == "c3":
		track1_c3_amount = path1_time * c3t3[0] /60
		track2_c3_amount = path2_time * c3t3[1] /60


		
		c3_amount = [track1_c3_amount,track2_c3_amount]

		return c3_amount	
def time_calculation(time_list):
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
		print time_difference
		print "Total Seconds: " + str(seconds)
			#print days
		print "Total Minutes: " + str(minutes)
		print "Total hours: "+ str(hours)
		
		#print total
	
	return total
	  
def track_path(coordinate_list,longi,lat):
		
	first_element_switch = False
	last_element_switch = False
	initial_time = None
	final_time = None
	time_list = []
	for i in range(0,len(coordinate_list)):
		x, y = coordinate_list[i][1],coordinate_list[i][2]
				
		if check_point(x,y,longi,lat):
			print str(Point(y,x)) + " is inside Track 3" + " at " + coordinate_list[i][0]
			if first_element_switch == False:
				initial_time = coordinate_list[i][0]
				first_element_switch = True
				last_element_switch = True
							
						
			if last_element_switch == True:
				final_time = coordinate_list[i][0]
						
		else:
			first_element_switch = False
			t = (initial_time,final_time)
			time_list.append(tuple(t))
	t1 = (initial_time,final_time)
	time_list.append(tuple(t1))
#        print set(time_list)
			
	return time_list

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def car_path():
	return render_template('index.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
	jsdata = request.form['trackname']
	print jsdata
	return jsdata

@app.route('/test/', methods=['GET','POST'])
def test():
	clicked=None
	print "here"
	if request.method == "POST":
		clicked=request.json['data']
	return render_template('test.html')
@app.route('/newmethod', methods = ['POST'])
def get_newpost_javascript_data():
	jsdata = request.form['options']
	print jsdata
	return jsdata

@app.route('/bosch',methods=['POST','GET'])
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
			print coordinate_list
			for row in coordinate_list:
				for k in (1,2):
					row[k] = float(row[k])
			final_total_t1 = 0
			final_total_t2 = 0
			final_total_t3 = 0
		#csv_input = csv.reader(stream)

		#print csv_input
		#for row in csv_input:
		#	print row
		
			if (select == "t1"):
				path1 = track_path(coordinate_list,lons_vect,lats_vect)
				path2 = track_path(coordinate_list,lons_vect2,lats_vect2)
				path3 = track_path(coordinate_list,lons_vect3,lats_vect3)
				path4 = track_path(coordinate_list,lons_vect4,lats_vect4)



				path_total1 = time_calculation(path1)
				path_total2 = time_calculation(path2)
				path_total3 = time_calculation(path3)
				path_total4 = time_calculation(path4)

				path_total_t1 = [path_total1,path_total2,path_total3,path_total4]
				
				for i in range(0,len(path_total_t1)):
					final_total_t1+=path_total_t1[i]

				print final_total_t1



				print "The total amount for track 1 is : " + str(path_total1)
				print "The total amount for track 2 is : " + str(path_total2)
				print "The total amount for track 3 is : " + str(path_total3)
				print "The total amount for track 4 is : " + str(path_total4)

				amt = rate_calculation_t1(oem,path_total1,path_total2,path_total3,path_total4)
				final_amt = 0
				for i in range(0,len(amt)):
					final_amt += amt[i]

				print "Total amount is : " + str(final_amt)

				return render_template("bosch.html",calculation=calculation,path_and_track_total = zip(path_total_t1,amt),final_total=final_total_t1, final_amount = final_amt,site=select,company=oem)

			elif(select == "t2"):

				path5 = track_path(coordinate_list,lons_vect5,lats_vect5)
				path6 = track_path(coordinate_list,lons_vect6,lats_vect6)

				path_total5 = time_calculation(path5)
				path_total6 = time_calculation(path6)

				path_total_t2 = [path_total5,path_total6]

				print path_total_t2

				for i in range(0,len(path_total_t2)):
					final_total_t2+=path_total_t2[i]

				print final_total_t2


				return render_template("bosch.html",calculation=calculation,path_total = path_total_t2,final_total=final_total_t2,site=select,company=oem)

			elif(select == "t3"):

				path7 = track_path(coordinate_list,lons_vect7,lats_vect7)
				path8 = track_path(coordinate_list,lons_vect8,lats_vect8)

				path_total7 = time_calculation(path7)
				path_total8 = time_calculation(path8)

				path_total_t3 = [path_total7,path_total8]

				print path_total_t3

				for i in range(0,len(path_total_t3)):
					final_total_t3+=path_total_t3[i]

				print final_total_t3


				return render_template("bosch.html",calculation=calculation,path_total = path_total_t3,final_total=final_total_t3,site=select,company=oem)
			else:
				print "Error"
		

	


if __name__ == '__main__':
	app.debug = True
	app.run()
	app.run(debug = True)
