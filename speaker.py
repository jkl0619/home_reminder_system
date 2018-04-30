import gTTS
import os

#message callback function
def on_message(client, userdata, message):
	serverMessage = str(message.payload.decode("utf-8"))
	tts = gTTS(text=serverMessage, lang='en', slow=False)		#serverMessage into google's text to speech data type
	tts.save("alert.mp3")										#save the tts file 
	os.system("omxplayer alert.mp3")							#play the mp3 file
	
def on_connect(client, userdata, flags, rc):
	client.subscribe(topic)

#MQTT client setup
host = "127.0.0.1"
client_name = 'sink_sensor_0'
topic = "ALERT_SINK_0"
Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client = mqtt.Client(client_name)
client.on_message = on_message
client.on_connect = on_connect
client.connect(host, port=1883, keepalive=60, bind_address="")


#look for messages
client.loop_forever()

