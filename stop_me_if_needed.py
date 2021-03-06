import os
import sys
import tempfile
import subprocess
import contextlib


# https://stackoverflow.com/questions/6194499/pushd-through-os-system
@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


with tempfile.TemporaryDirectory() as tmpdir, pushd(tmpdir):
    subprocess.run(
        ["git", "clone", "--depth=1", "https://github.com/regro/circle_worker.git"],
        check=True)

    if os.path.exists(os.path.join("circle_worker", "please.go")):
        go = True
    else:
        go = False

if not go:
    print("I could not find the file 'please.go' on master! Stopping!")
    sys.exit(1)
