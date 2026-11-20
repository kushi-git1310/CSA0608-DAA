#!/bin/sh
# Runs every task, stores the console output and regenerates the screenshots.
# Usage:  sh run_all.sh        (Python 3.8+ ; Pillow is needed only for make_screenshots.py)
mkdir -p outputs screenshots
for f in task1_word_wrap task2_greedy_vs_dp task3_routing task4_assembly_line task5_mst task6_tsp; do
  n=$(echo $f | cut -c5)
  echo "Running $f.py ..."
  python3 $f.py > outputs/task${n}_output.txt 2>&1 || echo "  FAILED: $f"
done
python3 make_screenshots.py
