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


heartbeat_time_delta = None

with tempfile.TemporaryDirectory() as tmpdir, pushd(tmpdir):
    subprocess.run(
        ["git", "clone", "https://github.com/regro/circle_worker.git"],
        check=True)

    with pushd("circle_worker"):
        if os.path.exists("please.go"):
            go = True
        else:
            go = False

        subprocess.run("git checkout heartbeats", check=True, shell=True)

        # we never go if we are told to stop
        if go:
            heartbeat_file = sys.argv[1] + ".json"
            if not os.path.exists(heartbeat_file):
                go = False
            else:
                with open(heartbeat_file, "r") as fp:
                    heartbeat = json.load(fp)["heartbeat"]

                heartbeat_time_delta = time.time() - heartbeat
                if heartbeat_time_delta < THREEHOURS:
                    go = False

if not go:
    print(
        "I could not find the file 'please.go' on master or "
        "the heartbeat was too soon (%s minutes)! Not triggering!" % (
            (heartbeat_time_delta or -60)/60
        )
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

    if r.status_code != 201:
        print("the next worker could not be started!")
        print("response:\n%s" % r.status_code)
        r.raise_for_status()
    else:
        print("the next worker was started!")
