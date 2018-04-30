import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import pin_setup
import time
import database

#system information
info = database.system_information

#GPIO setup
pins = pin_setup.pins
GPIO.setmode(pins['pinmode'])
GPIO.setup(pins['data_in'], GPIO.IN)

#MQTT setup
client_name = 'motion_sensor_0'
topic = "ROO_STATUS"
Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client =mqtt.Client(client_name)
client.connect(host, port=1883, keepalive=60, bind_address="")
subscribe(topic, qos=0)


#calibration
print("calibrating sensor\n";
calibrationTime = 30;    		#data sheet asks for a 10s to 60s calibration time
for x in range (0, calibrationTime):
	print(".\n");
	time.sleep(1)
print("done\n");
time.sleep(1)
print("SENSOR ACTIVE\n");


#motion detection
inRoom = False
sent = False
while 1:			#constantly check if the PIR sensor has seen motion
	if GPIO.input(pins['data_in']) == GPIO.HIGH):			#sensor will display a high value in the event that there is any motion detected
		time.sleep(.5)									#slight delay since the sensor will have a high value for about .3s
		if inRoom == False										#if they ARE NOT currently in the room, it means they are passing the sensor to ENTER the room
			sent = False
			inRoom = True	
			print('%s has entered the room, turning on the lights', info['name'])
		if inRoom:												#if they ARE currently in the room, it means they are passing the sensor again to LEAVE the room 		
			Sent = False
			inRoom = False	
			print('%s has left the room, turning off the lights', info['name'])
		######
		# send data to the server that says the user is now in this room
		######
		
		
	if inRoom and not sent:						#while the user is in the room, the lights should be on
		sent = True
		#####
		# use lights.py or whatever to turn on the lights in this room
		#####
		
	if not inRoom and not sent:
		#####
		# use lights.py or whatever to turn off the lights in this room
		#####
		