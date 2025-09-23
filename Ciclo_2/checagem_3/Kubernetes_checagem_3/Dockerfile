FROM python:3.8.8-slim-buster

WORKDIR /app

COPY . app.py /app/

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
