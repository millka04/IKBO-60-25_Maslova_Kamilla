#!/bin/sh
DIR="$(dirname "$0")"
if [ "$1" = "test" ]; then
    PYTHONPATH="$DIR/src" python3 -m unittest discover -s "$DIR/tests" -v
else
    python3 "$DIR/src/main.py" "$@"
fi