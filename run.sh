#!/bin/bash
python raytracer.py
# open up the created file (using that it's the most recent)
most_recent=$(ls -t | head -n1 | grep .png)
if [ "$most_recent" != "" ]
then
xdg-open $most_recent
fi
