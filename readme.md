# cloudflare-speedtest-mqtt
![Image Build Status](https://img.shields.io/github/workflow/status/ccmpbll/cloudflare-speedtest-mqtt/Docker%20Image%20CI?style=flat-square) ![Docker Image Size](https://img.shields.io/docker/image-size/ccmpbll/cloudflare-speedtest-mqtt/latest?style=flat-square) ![Docker Pulls](https://img.shields.io/docker/pulls/ccmpbll/cloudflare-speedtest-mqtt.svg?style=flat-square) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)

A simple container designed to send JSON formatted CloudFlare speedtest results over MQTT.

Heavily influenced by and some code borrowed from [https://github.com/simonjenny/fastcom-mqtt](https://github.com/simonjenny/fastcom-mqtt). Uses [https://github.com/tevslin/cloudflarepycli](https://github.com/tevslin/cloudflarepycli) to perform the speedtest. Shoutout to these two for building excellent projects. 



Required environment variables:

MQTT_SERVER : IP address of MQTT server

MQTT_TOPIC : Topic for speedtest results

SLEEP : Seconds between speedtest runs


Optional environment variables:

MQTT_USER: MQTT username

MQTT_PASS: MQTT password


Example:
```
docker run -d -e MQTT_TOPIC='cfspeedtest/results' -e MQTT_SERVER_='192.168.1.10' -e SLEEP='3600' ccmpbll/cloudflare-speedtest-mqtt:latest
```
