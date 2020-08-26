import os
import sys
import github


gh = github.Github(os.environ["PASSWORD"])

repo = gh.get_repo("regro/circle_worker")

repo.create_issue(
    title="failed circle job %s" % os.environ["CIRCLE_BUILD_NUM"],
    body="""
Hey!

It appears that the bot `%s` job failed! :(

I hope it is not too much work to fix but we all know that is never the case.

Have a great day!

job url: %s

""" % (sys.argv[1], os.environ["CIRCLE_BUILD_URL"])
)
