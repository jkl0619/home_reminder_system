import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pin_setup
import time
import database

#system information
info = database.system_information

#GPIO setup
pins = pin_setup.pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins['data_in'], GPIO.IN)
GPIO.setup(pins['led_pin'], GPIO.OUT)

#MQTT setup
mqttc = mqtt.Client()
mqttc.connect("m2m.eclipse.org", 1883)

#calibration
print("calibrating sensor\n");
calibrationTime = 3;    		#data sheet asks for a 10s to 60s calibration time
for x in range (0, calibrationTime):
	print(str(x) + "\n");
	time.sleep(1)
print("done\n");
time.sleep(1)
print("SENSOR ACTIVE\n");


#motion detection
inRoom = False
sent = False
lights = False
GPIO.output(pins['led_pin'], GPIO.LOW)
while 1:			#constantly check if the PIR sensor has seen motion
	if GPIO.input(pins['data_in']) == GPIO.HIGH:			#sensor will display a high value in the event that there is any motion detected
		time.sleep(7.5)										#slight delay since the sensor will have a high value for about 5s
		if inRoom == False:									#if they ARE NOT currently in the room, it means they are passing the sensor to ENTER the room
			sent = False
			inRoom = True	
			print(info['name'] + ' has entered the room, turning on the lights')
		elif inRoom:											#if they ARE currently in the room, it means they are passing the sensor again to LEAVE the room 		
			Sent = False
			inRoom = False	
			print(info['name'] + ' has left the room, turning off the lights')
	
		
		
	if inRoom and not sent:						#while the user is in the room, the lights should be on
		print('sending roomstatus to server: room_0 entered')
		sent = True
		decoded_message = 'User has entered room 0'
		publish.single("netapphome/roomstatus/0", decoded_message, hostname="m2m.eclipse.org")					#send a message that the user is now in room 0
		GPIO.output(pins['led_pin'], GPIO.HIGH)
		lights = True
		
	elif not inRoom and lights:
                lights = False
                GPIO.output(pins['led_pin'], GPIO.LOW)

