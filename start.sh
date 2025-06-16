#!/bin/bash

# Iniciar backend
cd backend
sudo python3 run.py &

# Aguardar backend iniciar
sleep 5

# Iniciar frontend
cd ../frontend
python3 main.py &

# Manter script rodando
wait