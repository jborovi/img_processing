FROM ubuntu:20.04 as opencv
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague
RUN apt update
RUN apt install libopencv-dev python3-opencv python3-pip -y
FROM opencv as app_common
COPY ./img_processing_common/src /app_common
COPY ./img_processing_common/requirements.txt /app_common/
RUN pip3 install --upgrade --no-cache-dir -r /app_common/requirements.txt
WORKDIR /app_common
RUN python3 setup.py install
FROM app_common as module_color
COPY ./module_color/requirements.txt /app/requirements.txt
RUN pip3 install --upgrade --no-cache-dir -r /app/requirements.txt
COPY ./module_color/src /app
WORKDIR /app
CMD ["python3", "-m", "module_color.main"]
