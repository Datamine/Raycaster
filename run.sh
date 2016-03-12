#!/bin/bash
python raytracer.py
# open up the created file (using that it's the most recent)
most_recent=$(ls -t | head -n1)
xdg-open $most_recent
