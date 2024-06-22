FROM debian:bookworm-slim
LABEL Name=cloudflare-speedest-mqtt
LABEL maintainer="Chris Campbell"

RUN apt update && apt full-upgrade -y
RUN apt install python3 python3-numpy python3-requests gnupg mosquitto-clients -y
RUN apt clean && apt autoremove -y

COPY cfspeedtest.py /opt
COPY cfspeedtestclass.py /opt
COPY speedtest.sh /usr/bin
RUN ["chmod", "+x", "/usr/bin/speedtest.sh"]

CMD /usr/bin/speedtest.sh