#!/bin/bash
while true
do
	echo "Running CloudFlare Speedtest..."
  
  	touch /tmp/speedtest-result
	cfspeedtest --json > /tmp/speedtest-result

	if [[ "${MQTT_PASS}" ]]; then
	echo "Sending Data to ($MQTT_SERVER)..."
		mosquitto_pub -u $MQTT_USER -P $MQTT_PASS -h $MQTT_SERVER -t $MQTT_TOPIC -f /tmp/speedtest-result
	else
	echo "Sending Data to ($MQTT_SERVER) with no authentication..."
		mosquitto_pub -h $MQTT_SERVER -t $MQTT_TOPIC -f /tmp/speedtest-result
	fi 
	
	echo "Cleaning up for the next run..."
	rm /tmp/speedtest-result
	
	echo "Sleeping for $SLEEP Seconds..."
	
	sleep $SLEEP 

done
