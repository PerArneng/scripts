#!/usr/bin/env python

# This script takes a nr of git repository folders and runs git log in them.
# It then collects statistics and outputs a csv representation to stdout
# containing the period YYYY-MM and commit statistics. For details run the
# command without any arguments

import sys
import subprocess
import re

if len(sys.argv) < 2:
    print("gitstats2csv: to few args")
    print("gitstats2csv: usage: git_stats.py <git repo folder...>")
    print("gitstats2csv: fmt: period;commits;unique_user_count;commits_per_user")
    sys.exit(1)

git_log_cmd = r'git --no-pager log --date=short --pretty=format:"%ad %ae"'
logpattern = re.compile('(\d\d\d\d)-(\d\d)-(\d\d) (.*)')
months = {}

class Stat:

    def __init__(self, period):
        self.period = period
        self.users = {}
        self.commits = 0

    def user_count(self):
        return len(self.users)

    def commits_per_user(self):
        return  float(self.commits) / self.user_count()

def register_line(line):
    match = logpattern.match(line)
    if match:
        year = match.group(1)
        month = match.group(2)
        email = match.group(4)

        yrmnth = "%s-%s" % (year, month)
        stat = months.get(yrmnth)

        if stat is None:
            stat = Stat(yrmnth)
            months[yrmnth] = stat

        stat.users[email] = email
        stat.commits = stat.commits + 1


for dir in sys.argv[1:]:

    output = subprocess.check_output(git_log_cmd, cwd=dir, shell=True)

    for line in output.splitlines():
        register_line(line)

for month in months.values():

    print("%s;%s;%s;%s" % (month.period, month.commits,
                           month.user_count(), month.commits_per_user()))
