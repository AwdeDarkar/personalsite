FROM alpine:3.10
MAINTAINER Ben Croisdale <bcroisdale@gmail.com>

# Basic
RUN apk update

# Install python core tools
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools

COPY ./requirements.txt /app/requirements.txt

# Software version management
ENV NGINX_VERSION=1.13.8-1~jessie
ENV SUPERVISOR_VERSION=3.0r1-1+deb8u1
ENV GUNICORN_VERSION=19.7.1
ENV GEVENT_VERSION=1.2.2

# Install database tools
RUN apk add --no-cache postgresql-dev musl-dev

# Install node core tools
RUN apk add --update nodejs npm

COPY package*.json /app/

WORKDIR /app

RUN apk add --no-cache nginx supervisor
RUN rm -rf /var/lib/apt/lists/*

# Install python modules
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir gunicorn==$GUNICORN_VERSION

# Install node modules
RUN npm install

# Copy files to the right locations
COPY . /app
COPY production/nginx.conf /etc/nginx/nginx.conf
COPY production/supervisord.conf /etc/supervisord/conf.d/supervisord.conf
COPY production/mime.types /etc/nginx/conf.d/mime.types
#COPY production/proxy.conf /etc/nginx/proxy.conf
#COPY production/fastcgi.conf /etc/nginx/fastcgi.conf
COPY production/gunicorn.config.py /app/gunicorn.config.py
COPY ./node_modules /var/www/node

# Make log directories
RUN mkdir /var/log/gunicorn
RUN mkdir /var/log/supervisord

# Build frontend
RUN npm run build
RUN cp -r ./website/static /var/www/static

# Configure Nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 5000
EXPOSE 5432
EXPOSE 50190

CMD ./docker/entry.sh prod
