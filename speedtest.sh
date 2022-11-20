#!/bin/bash
while true
do
	echo "Running CloudFlare Speedtest..."
  
  	touch /tmp/speedtest-result
	cfspeedtest --json > /tmp/speedtest-result
  	RESULT=$(cat /tmp/speedtest-result)

	if [[ "${MQTT_PASS}" ]]; then
	echo "Sending Data to MQTT ($MQTT_SERVER)..."
		mosquitto_pub -u $MQTT_USER -P $MQTT_PASS -h $MQTT_SERVER -t $MQTT_TOPIC -m $RESULT
	else
	echo "Sending Data to MQTT ($MQTT_SERVER) -  No Auth"
		mosquitto_pub -h $MQTT_SERVER -t $MQTT_TOPIC -m $RESULT
	fi 

	echo "Sleeping for $SLEEP Seconds..."
	
	sleep $SLEEP 

done
