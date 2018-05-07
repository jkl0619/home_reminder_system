How to use this system.

1. MQTT_Lens is used to control the threshold of other sensors.

https://www.hivemq.com/blog/mqtt-toolbox-mqtt-lens


Each sensor should be listening to a specific topic and respond to the changes in the threshold using callbacks.

2. The pi systems need to have paho-mqtt (pip3 install paho-mqtt) as well as gTTS.

3. One central server.py should be run, and the pi in the rooms need to have specific_sensor.py system running.

