FROM pytorch/pytorch:latest 

WORKDIR /usr/src/app
COPY machine-learning/. ./
COPY containers/hatespeech.train/bootstrap.sh ./
RUN sh bootstrap.sh
