FROM python:3.8-alpine

COPY ./assets/* /opt/resource/
RUN chmod +x /opt/resource/*

ENV workdir /data
WORKDIR ${workdir}

RUN mkdir -p ${workdir}
COPY ./setup.py ${workdir}
COPY ./youtube_upload ${workdir}/youtube_upload
COPY ./bin ${workdir}/bin
RUN chmod +x ${workdir}/bin/*
RUN pip install --upgrade google-api-python-client oauth2client progressbar2 && \
    python setup.py install && \
    apk add --update coreutils jq

ENTRYPOINT ["youtube-upload"]
