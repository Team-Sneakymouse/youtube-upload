FROM python:3.8-alpine

ENV workdir /data
WORKDIR ${workdir}

RUN mkdir -p ${workdir}
COPY . ${workdir}
WORKDIR ${workdir}
RUN pip install --upgrade google-api-python-client oauth2client progressbar2 && \
    python setup.py install && \
    apk add --update coreutils jq

ENTRYPOINT ["youtube-upload"]
