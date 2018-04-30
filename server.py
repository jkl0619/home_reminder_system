import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


# This is just to let you know that connect was established
def on_connect(mqttc, obj, flags, rc):
    print("connected to rc: " + str(rc))


#We have a server that will filter and handle messages.
# Things to subscribe to:
# 1. Different topics where the warning messages will be published to
# Things to publish to:
# 1. Different sensors to "Change" thresholds
# 2. Do things with the warning messages?

def on_message(mqttc, obj, msg):
    decoded_message = str(msg.payload, 'utf-8')
    if(msg.topic == "netapphome/bathroom"):
        publish.single("netapphome/bathroom/sensor", decoded_message, hostname="m2m.eclipse.org")
        print("the message: " + decoded_message + " was sent to the bathroom sensor")
    elif( msg.topic == "netapphome/kitchen"):
        publish.single("netapphome/kitchen/sensor", decoded_message, hostname="m2m.eclipse.org")
        print("the message: " + decoded_message + " was sent to the kitchen sensor")
    else:
        print("the message was: " + decoded_message)

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))



#attach the functions on to the mqtt broker.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish


#Connect to host, port
mqttc.connect("m2m.eclipse.org", 1883)
mqttc.subscribe("netapphome/#", 0)

mqttc.loop_forever()

while(1):
    dj = input("Please input something")
    print(str(dj) + " was the input")