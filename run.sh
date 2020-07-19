#!/bin/sh

export PYTHONPATH=$(pwd)/packages:$PYTHONPATH
python3 tools/tournament_client.py "$@" || echo "run error code: $?"
