FROM debian:bookworm-slim

USER root
ARG OUTPUT_DIRECTORY=/opt/partto
ARG INPUT_DIRECTORY=/opt/parttoin

RUN apt update && apt upgrade -y
RUN apt install curl software-properties-common -y
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash

RUN apt install -y nodejs
RUN mkdir -p ${OUTPUT_DIRECTORY}

WORKDIR $INPUT_DIRECTORY
ENTRYPOINT ["/bin/sh", "-c" , "npm run clean && npm ci && npm run build && cp -r ./build/* /opt/partto/"]
