import os
import sys
import github


gh = github.Github(os.environ["PASSWORD"])

repo = gh.get_repo("regro/circle_worker")

repo.create_issue(
    title="failed azure job %s" % os.environ["BUILD_BUILDID"],
    body="""
Hey @regro/auto-tick!

It appears that the bot `%s` job failed! :(

I hope it is not too much work to fix but we all know that is never the case.

Have a great day!

job url: IDK :/

""" % (sys.argv[1])
)
