#!/bin/sh

export PYTHONPATH=$(pwd)/packages:$PYTHONPATH

# python app/main.py "$@" || echo "run error code: $?"
python tools/tournament_client.py "$@" || echo "run error code: $?"
