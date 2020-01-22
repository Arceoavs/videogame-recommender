#!/bin/bash

python manage.py recreate_db
gunicorn -b 0.0.0.0:5000 --log-level INFO --timeout 300 manage:app

