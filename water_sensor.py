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
prevState = False
currentState = False
lastPinChange = int(time.time() * 1000)
pourStart = 0
pinChange = lastPinChange
pinDelta = 0

# time in ms.
global thresholdTime
thresholdTime = 3000

def on_message(mqttc, obj, msg):
    global thresholdTime
    decoded_message = str(msg.payload, 'utf-8')
    new_threshold = int(decoded_message)
    thresholdTime = new_threshold
    print("Threshold changed to " + thresholdTime)

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.connect("m2m.eclipse.org", 1883)
mqttc.subscribe("netapphome/kitchen/watersensor", 0)
mqttc.loop_start()


def countPulse(channel):
    global prevState
    global currentState
    currentTime = int(time.time() * 1000)



GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)
while True:
    if GPIO.input(FLOW_SENSOR):
        print("port " + FLOW_SENSOR + " is working")
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Leaving!")
