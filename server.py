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

currentRoom = 0
def on_message(mqttc, obj, msg):
    global currentRoom
    decoded_message = str(msg.payload, 'utf-8')
    if(msg.topic == "netapphome/roomstatus/0"):
        currentRoom = 0
        print("someone came into room: " + str(currentRoom) )
    elif (msg.topic == "netapphome/roomstatus/1"):
        currentRoom = 1
        print("someone came into room: " + str(currentRoom))
    elif (msg.topic == "netapphome/warning"):
        # Have ALL warning messages publish to this topic.
        # The message should be the details specific.
        topic_to_publish = "netapphome/alert/" + str(currentRoom)
        publish.single(topic_to_publish, decoded_message, hostname="m2m.eclipse.org")
        print(currentRoom)
    elif (msg.topic == "bojangle"):
        topisd = 2
        print(topisd)

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
