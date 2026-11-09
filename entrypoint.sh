#!/bin/sh
# entrypoint.sh

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

# Starte das Hauptskript
exec python3 main.py
