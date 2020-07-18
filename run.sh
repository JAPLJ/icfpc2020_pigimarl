#!/bin/sh

python tools/final_tournament.py "$@" || echo "run error code: $?"
