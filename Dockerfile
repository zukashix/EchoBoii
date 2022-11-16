# DOCKERFILE for echoboii-rw2 bot

# fetch ubuntu-focal
FROM ubuntu:18.04

# refresh apt repo
RUN apt update

# install dependencies
RUN apt install python3.8 -y
RUN apt install libpython3.8-dev -y
RUN apt install python3-pip -y
RUN apt install libopus0 ffmpeg -y
RUN apt install libffi-dev

# create working environment
RUN mkdir app
RUN cd app
WORKDIR /app
RUN mkdir plugins
RUN mkdir lib
RUN mkdir data

# add project files
COPY bot.py .
COPY requirements.txt .
COPY plugins plugins
COPY lib lib
COPY data data

# install pip requirements
RUN python3.8 -m pip install multidict attrs yarl async_timeout cchardet
RUN python3.8 -m pip install aiosignal
RUN python3.8 -m pip install -r requirements.txt

# run bot
CMD python3.8 bot.py
