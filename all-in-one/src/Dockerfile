FROM python:3

RUN apt-get update && \
    apt-get install -y libasound2-dev alsa-utils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/python/

COPY .asoundrc /home/python/.asoundrc

RUN pip install influxdb-client pms5003 matplotlib ltr559 python-dotenv

CMD ["python", "decibel-meter.py"]