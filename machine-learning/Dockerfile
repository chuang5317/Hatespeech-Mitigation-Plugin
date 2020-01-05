FROM python:3.6

RUN pip install sklearn spacy flask pandas boto3
RUN python -m spacy download en_core_web_md

COPY ds_logistic.py ./
COPY dataset ./dataset

COPY main.py ./
COPY hate_speech_classifier ./
COPY hate_speech_CountVectorizer ./

EXPOSE 8081
CMD ["python", "main.py"]
