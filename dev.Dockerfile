FROM alpine:3.10
MAINTAINER Ben Croisdale <bcroisdale@gmail.com>

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

# Install node core tools
RUN apk add --update nodejs npm

COPY package*.json /app/

WORKDIR /app

RUN echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list
RUN wget https://nginx.org/keys/nginx_signing.key -O - | apt-key add -
RUN apk add --no-cache nginx=$NGINX_VERSION \
                       supervisor=$SUPERVISOR_VERSION \
&& rm -rf /var/lib/apt/lists/*

# Install python modules
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn==$GUNICORN_VERSION gevent==$GEVENT_VERSION

# Install node modules
RUN npm install

# Copy files to the right locations
COPY . /app
COPY production/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY production/mime.types /etc/nginx/conf.d/conf/mime.types
COPY production/proxy.conf /etc/nginx/proxy.conf
COPY production/fastcgi.conf /etc/nginx/fastcgi.conf
COPY production/gunicorn.config.py /app/gunicorn.config.py
COPY ./website/static /static
COPY ./node_modules /node

# Build frontend
RUN npm run dev

# Configure Nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 5000

CMD ./entry.sh dev
CMD python3 manage.py run
