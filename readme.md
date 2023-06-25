# cloudflare-speedtest-mqtt
![Image Build Status](https://img.shields.io/github/actions/workflow/status/ccmpbll/cloudflare-speedtest-mqtt/docker-image.yml?branch=main) ![Docker Image Size](https://img.shields.io/docker/image-size/ccmpbll/cloudflare-speedtest-mqtt/latest) ![Docker Pulls](https://img.shields.io/docker/pulls/ccmpbll/cloudflare-speedtest-mqtt.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg)

A simple container designed to send JSON formatted CloudFlare speedtest results over MQTT.

#### UPDATE 06/25/2023:

I originally used [tevslin/cloudflarepycli](https://github.com/tevslin/cloudflarepycli) to perform the speedtest. However, the original author used a web service (ipdatabase.com) to return the internet service provider information for the current WAN IP address. In the last few days, that service has completely disappeared from the internet, causing errors when trying to run a speedtest. An [issue](https://github.com/tevslin/cloudflarepycli/issues/5) was filed describing this behavior back in November 2022, but no changes were made and no response was given. Since I am not certain this project is being actively maintained, I moved some of that code directly into my project, with some modifications.

#### Required environment variables:

MQTT_SERVER : IP address of MQTT server

MQTT_TOPIC : Topic for speedtest results

SLEEP : Seconds between speedtest runs

#### Optional environment variables:

MQTT_USER: MQTT username

MQTT_PASS: MQTT password

#### Example:
```
docker run -d -e MQTT_TOPIC='cfspeedtest/results' -e MQTT_SERVER_='192.168.1.10' -e SLEEP='3600' ccmpbll/cloudflare-speedtest-mqtt:latest
```

#### Telegraf Config Example

I use Telegraf to get this data into my InfluxDB instance. Below is an excerpt from my Telegraf config that shows how I accomplish this. 
I freely admit that I am not an expert here, so if there is an easier or simpler way to handle this, I am *very* open to suggestions.

```TOML
[[inputs.mqtt_consumer]]
name_override = "<WHAT YOU WANT THE INFLUXDB TABLE TO BE CALLED>"
servers = ["tcp://<YOUR MQTT SERVER IP>:1883"]
topics = ["<YOUR MQTT TOPIC>"]
data_format = "json_v2"
[[inputs.mqtt_consumer.json_v2]]
[[inputs.mqtt_consumer.json_v2.field]]
path = "your_ip.value"
rename = "wan_ip"
type = "string"
[[inputs.mqtt_consumer.json_v2.field]]
path = "your_ISP.value"
rename = "service_provider"
type = "string"
[[inputs.mqtt_consumer.json_v2.field]]
path = "test_location_code.value"
rename = "test_location_code"
type = "string"
[[inputs.mqtt_consumer.json_v2.field]]
path = "test_location_city.value"
rename = "test_location_city"
type = "string"
[[inputs.mqtt_consumer.json_v2.field]]
path = "latency_ms.value"
rename = "latency_ms"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "Jitter_ms.value"
rename = "jitter_ms"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "100kB_download_Mbps.value"
rename = "100kB_download_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "1MB_download_Mbps.value"
rename = "1MB_download_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "10MB_download_Mbps.value"
rename = "10MB_download_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "25MB_download_Mbps.value"
rename = "25MB_download_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "90th_percentile_download_speed.value"
rename = "90th_percentile_download_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "100kB_upload_Mbps.value"
rename = "100kB_upload_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "1MB_upload_Mbps.value"
rename = "1MB_upload_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "10MB_upload_Mbps.value"
rename = "10MB_upload_Mbps"
type = "float"
[[inputs.mqtt_consumer.json_v2.field]]
path = "90th_percentile_upload_speed.value"
rename = "90th_percentile_upload_Mbps"
type = "float"

```
