FROM alpine:3.20

ENV DJANGO_DEBUG=False
ARG SOURCE_DIRECTORY=/opt/partto
ARG VOLUME_DIRECTORY=/var/partto
ENV PART_TO_DATA_DIRECTORY=$VOLUME_DIRECTORY

RUN mkdir -p $SOURCE_DIRECTORY
RUN mkdir -p $VOLUME_DIRECTORY
WORKDIR $SOURCE_DIRECTORY
COPY . &SOURCE_DIRECTORY

RUN apk update
RUN apk add --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --no-cache nginx
COPY ./nginx.conf /etc/nginx/
RUN apk add --no-cache sqlite
RUN apk add --no-cache make
#RUN adduser -D -g 'www' www
#RUN mkdir /www
#RUN chown -R www:www /var/lib/nginx
#RUN chown -R www:www /www

#PART_TO_DATA_DIRECTORY


RUN make build

RUN rc-service nginx start



EXPOSE 22222

ENTRYPOINT make runproduct
