# Worker for running the regro-cf-autotick-bot

[![CircleCI](https://circleci.com/gh/regro/circle_worker.svg?style=svg)](https://circleci.com/gh/regro/circle_worker)


# Starting and Stopping the Worker

In order to start the worker, make a commit to master with the file `please.go`
in the top-level directory.

If you want to stop the worker, simply delete this file and it will not restart
itself on the next round.
