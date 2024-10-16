This is an implementation of `cat` program in Python.

## Kata assignment

Remove as many source code lines as possible while keeping the tests passing. Use coverage tools to get data which source code lines are reached by the tests and which are not.

## Preparation steps
After having cloned the repository, ensure that the characterization test passes. Additionally, make sure that the coverage tool is available and works.

- Run test `from characterization/test.py`. Adjust the reference if it has drifted away.
- Install `python-coverage` or check that it is already available on your PATH.

Here is how you ensure that the coverage tool for Python is available.
- Check if `python3-coverage` or `coverage3` are already available in your environment. If either of these binaries is usable, you are good to go. Otherwise, go to the next step.
- Set up HTTP and HTTPS proxies in your shell as needed.
- Run `pip3 install coverage` as a non-privileged user to install the new Python package.
- Check that `$HOME/.local/bin/coverage-3.9` (`change 3.9` to your specific version of Python) is present and usable.

## To collect coverage 

- `python3-coverage erase` // your script might be called coverage3
- `characterization/collect-coverage.py`
  - Make sure to run it from the top level of the repository, otherwise it might collect report for the test harness files.
- `python3-coverage html`

Open file `htmlcov/index.html` and drill down into `cat.py`.

