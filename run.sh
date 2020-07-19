#!/bin/sh

python3 tools/tournament-client.py "$@" || echo "run error code: $?"
