FROM ubuntu:22.04
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"
ARG MODEL=7b
ARG APP_DIR=/opt/codellama
# Setup workdir
WORKDIR ${APP_DIR}

# Setup dependencies
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install git subversion openjdk-8-jdk curl unzip build-essential cpanminus python3.10 python3.10-distutils -y
RUN apt-get install nvidia-driver-525 nvidia-dkms-525 -y
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Copy files

COPY CodeLlama-${MODEL}-Instruct/ ${APP_DIR}
COPY llama ${APP_DIR}
COPY requirements.txt ${APP_DIR}
COPY cerberus.py ${APP_DIR}

# Install python dependencies
RUN pip3 install -r requirements.txt