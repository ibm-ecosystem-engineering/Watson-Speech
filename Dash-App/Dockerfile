FROM python:3.9
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get -y update && apt-get -y install libsndfile1 && pip3 install -r requirements.txt
ARG SERVICE_PORT=8052
ENV TTS_SERVICE_URL "http://localhost:1080/text-to-speech/api/v1/synthesize"
ENV SERVICE_PORT ${SERVICE_PORT}
EXPOSE ${SERVICE_PORT}
ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH
COPY ./*.py /app
COPY ./assets /app/assets
CMD ["python3","TTS_dash_app.py"]