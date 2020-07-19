#!/bin/sh

# python app/main.py "$@" || echo "run error code: $?"
# python app/naive_orbit/naive_orbit.py "$@" || echo "run error code: $?"
python app/approach_suiside/approach_suiside.py "$@" || echo "run error code: $?"
