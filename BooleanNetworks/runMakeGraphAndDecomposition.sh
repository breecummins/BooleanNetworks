#!/usr/bin/sh

python makegraphs.py
open domaingraph.png wallgraph.png
python graphdecomposition.py