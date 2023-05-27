FROM python:3.10.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/dating-web-app

COPY ./req.txt /usr/dating-web-app/req.txt

RUN pip3 install -r /usr/dating-web-app/req.txt

COPY . /usr/dating-web-app

RUN python3 manage.py migrate

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]