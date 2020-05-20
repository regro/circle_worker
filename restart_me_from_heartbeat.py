import os
import sys
import tempfile
import subprocess
import contextlib
import json
import time

import requests

THREEHOURS = 3 * 60 * 60


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

    # we never go if we are told to stop
    if go:
        heartbeat_file = os.path.join("circle_worker", sys.argv[1] + ".json")
        if not os.path.exists(heartbeat_file):
            go = False
        else:
            with open(heartbeat_file, "r") as fp:
                heartbeat = json.load(fp)["heartbeat"]

            if time.time() - heartbeat < THREEHOURS:
                go = False

if not go:
    print(
        "I could not find the file 'please.go' on master or "
        "the heartbeat was too soon! Not triggering!"
    )
else:
    print("Starting the next worker...")
    r = requests.post(
        "https://circleci.com/api/v1.1/project/github/regro/circle_worker/tree/master",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"build_parameters": {"CIRCLE_JOB": sys.argv[1]}},
        auth=(os.environ["CIRCLE_TOKEN"], ""),
    )

    if str(r.status_code)[0] != 2:
        print("the next worker could not be started!")
        print("response:\n%s" % r.status_code)
        r.raise_for_status()
    else:
        print("the next worker was started!")
