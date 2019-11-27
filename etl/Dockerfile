FROM python:3.7

COPY . /etl

WORKDIR /etl

RUN pip install -r requirements.txt

# Run forever and ever
CMD ["tail", "-f", "/dev/null"]