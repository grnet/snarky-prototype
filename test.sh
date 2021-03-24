#!/bin/bash

python3 -m pytest --cov-report term-missing --ignore-glob=demo.py --cov=. $*
