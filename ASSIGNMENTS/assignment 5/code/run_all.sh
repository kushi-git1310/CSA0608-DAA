#!/bin/sh
# Runs every program and stores the real output in ../outputs
cd "$(dirname "$0")"
mkdir -p ../outputs
for f in b1_graph_colouring trace_demo b2_adversarial b3_set_cover b4_bin_packing; do
  echo "running $f ..."; python3 $f.py > ../outputs/$f.txt 2>&1
done
