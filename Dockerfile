FROM debian:bookworm-slim

USER root
ENV DJANGO_DEBUG=False
ARG VOLUME_DIRECTORY=/opt/partto
ENV PART_TO_DATA_DIRECTORY=/var/partto
ENV REACT_APP_PART_TO_API_BASE=
ENV NODE=$VOLUME_DIRECTORY/nenv/bin/nodejs
ENV NPM=$VOLUME_DIRECTORY/nenv/bin/npm
ENV NODE_ENV_PATH="PATH=$PATH:$VOLUME_DIRECTORY/nenv/bin"

RUN mkdir -p $PART_TO_DATA_DIRECTORY
RUN mkdir -p $VOLUME_DIRECTORY/recipeexamples
RUN mkdir -p $VOLUME_DIRECTORY/project
COPY ./recipeexamples/ $VOLUME_DIRECTORY/recipeexamples/
COPY ./project/ $VOLUME_DIRECTORY/project/
COPY ./version.toml $VOLUME_DIRECTORY/
COPY ./requirements.txt $VOLUME_DIRECTORY/
COPY ./Makefile $VOLUME_DIRECTORY/
WORKDIR $VOLUME_DIRECTORY

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y sqlite3
RUN apt-get install -y make

EXPOSE 20222

ENTRYPOINT ["/usr/bin/make", "-C", "/opt/partto", "-f", "/opt/partto/Makefile", "enterimage"]
