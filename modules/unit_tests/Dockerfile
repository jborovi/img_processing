FROM ubuntu:20.04 as opencv
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Prague
RUN apt update && apt install libopencv-dev python3-opencv python3-pip -y
FROM opencv as unit_tests
COPY ./img_processing_common/src /app_common
COPY ./img_processing_common/requirements.txt /app_common/
RUN pip3 install --upgrade --no-cache-dir -r /app_common/requirements.txt

COPY ./unit_tests/requirements.txt /requirements_test.txt
COPY ./module_input/requirements.txt /requirements_module_input.txt
COPY ./module_rgba/requirements.txt /requirements_module_rgba.txt
COPY ./module_color/requirements.txt /requirements_module_color.txt

RUN pip install --no-cache-dir -r /requirements_test.txt
RUN pip install --no-cache-dir -r /requirements_module_color.txt
RUN pip install --no-cache-dir -r /requirements_module_input.txt
RUN pip install --no-cache-dir -r /requirements_module_rgba.txt


COPY ./img_processing_common/src /app_common/src
COPY ./img_processing_common/requirements.txt /app_common/
WORKDIR /app_common/src
RUN pip install -e .

COPY ./module_input/src /app_module_input/src
WORKDIR /app_module_input/src
RUN pip install -e .
COPY ./module_rgba/src /app_module_rgba/src
WORKDIR /app_module_rgba/src
RUN pip install -e .

COPY ./module_color/src /app_module_color/src
WORKDIR /app_module_color/src
RUN pip install -e .

COPY ./unit_tests/test_data /tests/test_data
COPY ./unit_tests/tests /tests


WORKDIR /
ENTRYPOINT ["pytest"]
