#!/bin/bash

cd backend
python3 run.py &

sleep 3

cd ../frontend
python3 app.py &

wait