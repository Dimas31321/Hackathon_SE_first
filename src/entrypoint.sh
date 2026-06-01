#!/bin/sh
[ -f "./extended_src/query_sort.py" ] && [ -f "./extended_src/requirements.txt" ]
NO_EXTENDED_VERSION=$?
python -m src.main