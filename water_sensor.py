import RPi.GPIO as GPIO
import time, sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


#initialize sensors
FLOW_SENSOR = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP)

topic_to_publish = "netapphome/warning"

# initialize variables
global count
count = 0
global pouring
global lastPinState
global pinstate
global lastPinChange
global pinChange
global pinDelta

pouring = False
lastPinState = False
pinstate = False
lastPinChange = int(time.time() * 1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0

# time in ms.
global thresholdTime
thresholdTime = 5000

def on_message(mqttc, obj, msg):
    global thresholdTime
    decoded_message = str(msg.payload, 'utf-8')
    new_threshold = int(decoded_message)
    thresholdTime = new_threshold
    print("Threshold has changed")

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect("m2m.eclipse.org", 1883)
mqttc.subscribe("netapphome/kitchen/watersensor", 0)
mqttc.loop_start()

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING)

while True:
    global pinstate
    currentTime = int(time.time() * 1000)
    if GPIO.event_detected(FLOW_SENSOR):
        pinstate = True
    else:
        pinstate = False
    if (pinstate != lastPinState and pinstate == True):
        if (pouring == False):
            pourStart = currentTime
            print("pour has started")
        pouring = True
        # get the current time
        pinChange = currentTime
        pinDelta = pinChange - lastPinChange
    if (pouring == True and pinstate != lastPinState and (currentTime - lastPinChange) > thresholdTime):
        message = "The water has been left on for too long in the kitchen!"
        publish.single(topic_to_publish, message, hostname="m2m.eclipse.org")
        print("Message published")
    if (pouring == True and pinstate == lastPinState and (currentTime - lastPinChange) > 3000):
        # set pouring back to false. Essentially, if no input for about 3 seconds, then it is considered as to have stopped pouring.
        print("pouring has stopped")
        pouring = False
        pourTime = int((currentTime - pourStart)/1000) - 3
    lastPinChange = pinChange
    lastPinState = pinstate
