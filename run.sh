#!/bin/sh
export PYTHONPATH=$PYTHONPATH:./app

sleep 10

python app/initial_data.py

exec uvicorn --reload --host 0.0.0.0 --port 9090 app.main:app