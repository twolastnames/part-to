FROM debian:bookworm-slim

USER root
ENV DJANGO_DEBUG=False
ARG VOLUME_DIRECTORY=/var/partto
ENV PART_TO_DATA_DIRECTORY=$VOLUME_DIRECTORY
ENV REACT_APP_PART_TO_API_BASE=
ENV NODE=/var/partto/nenv/bin/nodejs
ENV NPM=/var/partto/nenv/bin/npm
ENV NODE_ENV_PATH="PATH=$PATH:/var/partto/nenv/bin"

RUN mkdir -p $VOLUME_DIRECTORY/project
COPY ./project/ $VOLUME_DIRECTORY/project/
COPY ./version.toml $VOLUME_DIRECTORY/
COPY ./requirements.txt $VOLUME_DIRECTORY/
COPY ./Makefile $VOLUME_DIRECTORY/
WORKDIR $VOLUME_DIRECTORY
RUN ls

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-virtualenv
RUN apt-get install -y python3-pip
RUN apt-get install -y sqlite3
RUN apt-get install -y make

RUN /usr/bin/make build

EXPOSE 20222

RUN ls
ENTRYPOINT ["/usr/bin/make", "-C", "/var/partto", "-f", "/var/partto/Makefile", "enterimage"]


