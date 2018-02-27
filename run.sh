#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR && python3 custom_speedtest.py >> speed.log 2>&1
