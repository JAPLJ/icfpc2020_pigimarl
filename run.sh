#!/bin/sh

python3 app/main.py "$@" || echo "run error code: $?"
