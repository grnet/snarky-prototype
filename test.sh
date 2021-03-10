#!/bin/bash

python3 -m pytest tests/ --cov-report term-missing --cov=. $*
