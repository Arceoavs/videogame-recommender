# this dockerfile is used for production deployments
FROM python:3.7

COPY . /web
WORKDIR /web

RUN pip install -r requirements.txt

# for the flask config
ENV FLASK_ENV=prod
EXPOSE 5000

ENTRYPOINT ["scripts/docker.prod.sh"]
