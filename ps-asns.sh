#!/bin/bash
date
python ps-asns.py
rc=$?; if [[ $rc != 0 ]]; then 
    echo "problem running traceroute. Exiting."
    exit $rc
fi
