#!/bin/sh

# python app/main.py "$@" || echo "run error code: $?"
python app/bunretsu_walk.py "$@" || echo "run error code: $?"
