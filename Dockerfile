FROM alpine:3.10

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD dockersetup.sh
CMD flask run
