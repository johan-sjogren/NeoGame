#!/usr/bin/sh

echo "Running AI module tests"
python AI/tests/test_script.py

echo "Running flask tests"
python test_flask.py

echo "Done"