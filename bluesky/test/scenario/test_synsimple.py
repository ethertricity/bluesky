"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
For inclusion with BlueSky upstream code:
https://github.com/ProfHoekstra/bluesky/, distributed under
GNU General Public License v3.

Author <ahfarrell@sparkl.com> Andrew Farrell
Tests Synthetic SIMPLE scenario
"""
from .conftest import sock_send
from . import init_snaplog, get_snaplog_contents
from .. import assert_fl


def synsimple_validate(snapshot_):
    # The new values for lat ([3]) or lon ([4]) are
    # in fact deterministic based on the simulation being
    # for roughly 60 seconds, where simdt is the same.
    # Expressing a tight range is sufficient to show the
    # direction of travel of the aircraft.
    #
    snapshot = snapshot_.split(',')
    if snapshot[1] == 'OWNSHIP':
        assert_fl(snapshot[3], -.4, .025)
        assert float(snapshot[4]) == 0.0
    else:
        assert float(snapshot[3]) == 0.0
        assert_fl(snapshot[4],  .4, .025)


def test_synsimple(sock, snaplog):
    init_ = init_snaplog(sock, snaplog)
    sock_send(sock, "SYN SIMPLE")
    contents = get_snaplog_contents(sock, snaplog, init_)
    synsimple_validate(contents[-2])
    synsimple_validate(contents[-1])


def test_synsimpled(sock, snaplog):
    init_ = init_snaplog(sock, snaplog)
    sock_send(sock, "SYN SIMPLED")
    contents = get_snaplog_contents(sock, snaplog, init_)
    synsimple_validate(contents[-2])
    synsimple_validate(contents[-1])
