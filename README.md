# Worker for running the regro-cf-autotick-bot

[![CircleCI](https://circleci.com/gh/regro/circle_worker.svg?style=svg)](https://circleci.com/gh/regro/circle_worker)
[![Build Status](https://dev.azure.com/conda-forge/regro/_apis/build/status/regro.circle_worker?branchName=azure-cron)](https://dev.azure.com/conda-forge/regro/_build/latest?definitionId=10250&branchName=azure-cron)

# Starting and Stopping the Worker

In order to start the worker, make a commit to master with the file `please.go`
in the top-level directory.

If you want to stop the worker, simply delete this file and it will not restart
itself on the next round.
