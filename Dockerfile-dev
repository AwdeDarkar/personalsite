FROM alpine:3.10

# Install python core tools
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools

COPY ./requirements.txt /app/requirements.txt

# Install node core tools
RUN apk add --update nodejs npm

COPY package*.json /app/

WORKDIR /app

# Install python modules
RUN pip3 install --no-cache-dir -r requirements.txt

# Install node modules
RUN npm install

COPY . /app

# Build frontend
RUN npm run dev

EXPOSE 5001

CMD ./entry.sh
CMD python3 manage.py run
