#!/bin/sh

python tools/tournament_client.py "$@" || echo "run error code: $?"
