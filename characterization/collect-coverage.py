#! /usr/bin/env python3
# Run characterization test but collect coverage
import sys
from test import main as real_main

def detect_coverage_command():
    from shutil import which
    for candidate in ("python3-coverage", "coverage3"):
        if which(candidate):
            return candidate
    raise Exception("No coverage binary found")


if __name__ == "__main__":
    coverage = detect_coverage_command()
    coverage_cmdline = [coverage, "run", "-a"]
    sys.exit(real_main(coverage_cmdline))
