FROM python:3-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 7777

ENTRYPOINT ["python3"]

CMD ["services.py"]