FROM python:3.8-buster

RUN mkdir /root/server

COPY requirements.txt /root/server
WORKDIR /root/server

# RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev
RUN pip3 install -r requirements.txt
# RUN apk del .build-deps gcc musl-dev libffi-dev

COPY . /root/server

EXPOSE 5000

CMD ["python", "app.py"]