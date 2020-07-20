#!/bin/sh

python3 tools/tournament_client.py "$@" || echo "run error code: $?"
