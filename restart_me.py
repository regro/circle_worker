import os
import pprint
import tempfile
import subprocess
import contextlib

import requests


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
else:
    print("Starting the next worker...")
    r = requests.post(
        "https://circleci.com/api/v2/project/github/regro/circle_worker/pipeline",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Circle-Token": os.environ['CIRCLE_TOKEN'],
        },
        json={"branch": "master"},
    )

    if r.status_code != 201:
        print("the next worker could not be started!")
        print("response:\n%s" % r.status_code)
        r.raise_for_status()
    else:
        print("the next worker was started!")
        print("response:\n%s" % pprint.pformat(r.json()))
