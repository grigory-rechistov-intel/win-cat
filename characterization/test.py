#! /usr/bin/env python3
# Compare outputs of commands against references

import os, sys
import difflib
import subprocess


pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(pathname + "/..")

def print_diff(a, b):
    d = difflib.Differ()
    result = list(d.compare(a.splitlines(keepends = True),
                            b.splitlines(keepends = True)))
    for line in result:
        print(line, end = "")
    print()

def get_input(input_file):
    with open(input_file, "rb") as f:
        return f.read().decode()   

def main(prefix):
    show_diff = True
    passed = 0
    failed = 0
    skipped = 0

    input_cases = (
        ([], "characterization/output0.ref"),
        (["characterization/input1"], "characterization/input1.ref"),
        (["-h"], "characterization/dash-h.ref"),
        (["-"], "characterization/output0.ref"),
        (["-v", "characterization/input-0x00"], "characterization/output-0x00-dash-v.ref"),
        (["-v", "characterization/input-0x20"], "characterization/output-0x20-dash-v.ref"),
        (["-v", "characterization/input-0x80"], "characterization/output-0x80-dash-v.ref"),
        (["-v", "characterization/input-0xa0"], "characterization/output-0xa0-dash-v.ref"),
        (["-A", "characterization/input-0x00"], "characterization/output-0x00-dash-A.ref"),
        (["-A", "characterization/input-0x20"], "characterization/output-0x20-dash-A.ref"),
        (["-A", "characterization/input-0x80"], "characterization/output-0x80-dash-A.ref"),
        (["-A", "characterization/input-0xa0"], "characterization/output-0xa0-dash-A.ref"),
        (["-T", "characterization/input-tab"], "characterization/output-tab-dash-T.ref"),
        (["-E", "characterization/input-newline"], "characterization/output-newline-dash-E.ref"),
        (["-", "characterization/input1"], "characterization/input1.ref"),
    )

    for cmdline, reference in input_cases:
        cmd = prefix + ["win_cat/cat.py"] + cmdline
        print(f"{' '.join(cmd)} <-> {reference}", end = "")
        try:
            output = subprocess.check_output(cmd,
                                             stdin=subprocess.DEVNULL,
                                             stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            output = e.output.decode()

        reference_text = get_input(reference)   
        
        if reference_text != output:
            print(" FAIL")
            failed += 1
            if show_diff:
                print_diff(reference_text, output)
        else:
            print(" PASS")
            passed += 1

    total = passed + failed + skipped
    print("-"* 80)
    print(f"Total {total}, passed {passed}, failed {failed}, skipped {skipped}")
    return failed

if __name__ == "__main__":
    prefix = [sys.executable]
    failed = main(prefix)
    sys.exit(failed != 0)
