FROM debian:latest
LABEL Name=cloudflare-speedest-mqtt Version=0.1
LABEL maintainer="Chris Campbell"

RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get install python3 python3-pip gnupg mosquitto-clients -y
RUN pip install cloudflarepycli bs4

COPY speedtest.sh /usr/bin
RUN ["chmod", "+x", "/usr/bin/speedtest.sh"]

CMD /usr/bin/speedtest.sh
