#!/bin/bash
while true
do
	echo "$(date +%D_%T) - Running CloudFlare Speed Test..."

	touch /tmp/speedtest-result
	python3 /opt/cfspeedtest.py --json > /tmp/speedtest-result
	#cfspeedtest --json > /tmp/speedtest-result

	if [[ "${MQTT_PASS}" ]]; then
	echo "$(date +%D_%T) - Sending Data to ($MQTT_SERVER)..."
		mosquitto_pub -u $MQTT_USER -P $MQTT_PASS -h $MQTT_SERVER -t $MQTT_TOPIC -f /tmp/speedtest-result
	else
	echo "$(date +%D_%T) - Sending Data to ($MQTT_SERVER) with no authentication..."
		mosquitto_pub -h $MQTT_SERVER -t $MQTT_TOPIC -f /tmp/speedtest-result
	fi

	echo "$(date +%D_%T) - Cleaning up for the next run..."
	rm /tmp/speedtest-result

	echo "$(date +%D_%T) - Sleeping for $SLEEP Seconds..."

	sleep $SLEEP

done