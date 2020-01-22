# Production

FROM python:3.7

COPY . /etl
WORKDIR /etl
RUN pip install -r requirements.txt

ENTRYPOINT ["./jobs.prod.sh"]