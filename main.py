import pandas as pd
import datetime as dt
import math
class postcodes():
	def __init__(self):
		self.data = pd.read_csv("postcodes.csv")
		self.latitude=0
		self.longitude=0
		self.postcode=""
	def find_coordinates(self):
		field=self.data.loc[(self.data["Postcode"]==self.postcode)]
		self.latitude = float(field["Latitude"])
		self.longitude = float(field["Longitude"]) 
	def get_coordinates(self):
		return(self.latitude,self.longitude)
	def set_postcode(self,tato_postcode):
		self.postcode=tato_postcode
		try:
			self.data.loc[(self.data["Postcode"]==tato_postcode)]
			self.find_coordinates()
			return True
		except:
			print("Not a valid postcode ye silly goose")
			return False

def delivery_time(miles):
	global drone_speed
	now=dt.datetime.now()
	day=now.day
	hour=now.hour
	minute=now.minute
	speed=drone_speed
	flight_time_hr=int(miles//speed)
	flight_time_mn=int((miles%speed)/speed*60)
	estimated_time_mn=minute+flight_time_mn
	if estimated_time_mn>=60:
		hour+=1
		estimated_time_mn-=60
	estimated_time_hr=hour+flight_time_hr
	if estimated_time_hr>=24:
		day+=1
		estimated_time_hr-=24
	print("delivered at "+date_str(estimated_time_hr)+":"+date_str(estimated_time_mn)+" on "+date_str(day)+"/"+date_str(now.month)+"/"+str(now.year))

def distance_to_customer():
	global post
	cust_coord = cust_address()
	company_address = (52.051938,1.180991)
	x = cust_coord[0] - company_address[0]
	y = cust_coord[1] - company_address[1]
	drone_travel_distance = ((x**2) + (y**2))**0.5
	return drone_travel_distance
def date_str(value):
	out=""
	if len(str(value)) == 1:
		out+="0"
	return out+str(value)
def distance():
    lat1, lon1 = (52.051938,1.180991)
    lat2, lon2 = cust_address()
    radius = 3959 # miles

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def cust_address():
	global post
	trail=False
	while trail == False:
		print("Solid pal, whats your postcode so we know where to send all this goodness?\nPlease can you put in the form XX11 1XX or XX1 1XX")
		trail = post.set_postcode(str(input()).upper())
	return (post.get_coordinates()) # customers location

def drone_reset():
	data=pd.read_csv("Drones.csv")
	for row in range(0,len(data)):
		data.iloc[row,4]='yes'
	data.to_csv('Drones.csv', mode='w',header=["Name","Colour","Max capacity(potatoes)","Max speed(mph)","availability"],index=False)
	print("CSV availability reset")

def drone():
	global no_tato
	global drone_speed
	data = pd.read_csv("Drones.csv")
	drone_mini = data.loc[(data["Colour"]=="White")] 
	drone_med = data.loc[(data["Colour"]=="Black")]
	drone_big = data.loc[(data["Colour"]=="Red")]
	drone,no_mini,no_mid="",False,False
	if no_tato > 0 and no_tato <11:
		for d in drone_mini:
			drone = drone_mini.loc[(drone_mini["availability"]=="yes")]
		if drone.empty==True:
			no_mini=True
	if (no_tato > 10 and no_tato <21) or (no_mini==True):
		for d in drone_med:
			drone = drone_med.loc[(drone_med["availability"]=="yes")] 
		if drone.empty==True:
			no_mid=True
	if (no_tato > 20 and no_tato <31) or (no_mid==True):
		drone = drone_big.loc[(drone_big["availability"]=="yes")]
		if drone.empty==True:
			return True
	x = drone.sample()
	drone_speed=x.iloc[0,3]
	print("Your taters are being delivered by "+str(x.iloc[0,0]))
	row=int(x.index.values)
	data.iloc[row,4]='no'
	data.to_csv('Drones.csv', mode='w',header=["Name","Colour","Max capacity(potatoes)","Max speed(mph)","availability"],index=False)

#POTATOES WEIGH 350G
post = postcodes()
print("How many of our scrumptious LANKEY'S MONSTA TATERS?") 
no_tato = input()
if no_tato == "reset":
	drone_reset()
else:
	while no_tato.isdigit() == False or int(no_tato) > 30 or int(no_tato) <= 0:
		if no_tato.isdigit() == False:
			print("need a number not words ya silly goose")
		elif int(no_tato) > 30:
			print("Sorry our drone canny handle that many potatoes sir, our maximum delivery is 30 taters")
		elif int(no_tato) <= 0:
			print("What are you doin you donkey! Order some potatoes... plz x")
		no_tato = input()
	no_tato=int(no_tato)
	tato_cost = no_tato*0.50
	miles = distance()
	miles_cost= 0.05*miles
	total_cost=tato_cost+miles_cost
	counter = 0
	tc = str(total_cost)
	for x in tc:
		counter = counter +1
		if x == ".":
			break
	counter = counter + 2
	print("total cost is: £"+ str(tc[0:counter]))
	a=drone()
	if a != True:
		delivery_time(miles)
	else:
		print("no available drones at the minute")
		drone_reset()
