# DOCKERFILE for echoboii-rw2 bot

# fetch base image
FROM python:3.8-bullseye

# refresh apt repo
RUN apt update

# install dependencies
RUN apt install libopus0 ffmpeg -y

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

# write docker build data
RUN rm -f data/build.json
RUN touch data/build.json
RUN echo '{"CurrentBuild":"Default-Ub-Docker"}' > data/build.json

# install pip requirements
RUN python -m pip install -r requirements.txt

# run bot
CMD python bot.py
