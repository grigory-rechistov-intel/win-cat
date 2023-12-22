#! /usr/bin/env python3
# Run characterization test but collect coverage
import sys
from test import main as real_main

if __name__ == "__main__":
    coverage_cmd = ["python3-coverage", "run", "-a"]
    sys.exit(real_main(coverage_cmd))
