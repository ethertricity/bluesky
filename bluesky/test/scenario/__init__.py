"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
For inclusion with BlueSky upstream code:
https://github.com/ProfHoekstra/bluesky/, distributed under
GNU General Public License v3.

Author <ahfarrell@sparkl.com> Andrew Farrell
Scenario test functionality.
"""
import os
from time import sleep
from .conftest import sock_send
from .. import wait_for


def init_snaplog(sock, snaplog):
    init_dir = set(os.listdir(snaplog))
    sock_send(sock, "SNAPLOG ON 5")
    sleep(5)  # back off for a moment
    return init_dir


def get_snaplog_contents(sock, snaplog, init_, sleep_=60):
    sleep(sleep_)
    sock_send(sock, "SNAPLOG OFF")

    snaplog_file = list(
        set(os.listdir(snaplog)) - init_)[0]
    snaplog_path =  os.path.join(snaplog, snaplog_file)

    wait_for(
        lambda: os.stat(snaplog_path).st_size > 0)

    pos = None
    contents = []
    with open(snaplog_path, 'r') as snapfile:
        while True:
            line = snapfile.readline().strip()
            newpos = snapfile.tell()

            if pos == newpos:
                return contents

            pos = newpos
            contents.append(line)
