From python:3.9

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /example_app

WORKDIR /example_app

# TODO use dockerignore file!
RUN rm ./example_app/.env

ENV PORT 8080

CMD gunicorn --bind :$PORT example_app.wsgi:application