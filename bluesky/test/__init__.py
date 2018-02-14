"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.
For inclusion with BlueSky upstream code:
https://github.com/ProfHoekstra/bluesky/, distributed under
GNU General Public License v3.

Author <ahfarrell@sparkl.com> Andrew Farrell
Common test functionality.
"""
from __future__ import print_function
import inspect
import time


def assert_fl(result, reference, threshold=0.49):
    """
    Tests whether the absolute (i.e. distance from zero) difference
    between a result and a reference value is less than a provided threshold.

    If not provided, the default threshold of 0.49 is used.
    """
    assert abs(float(result) - reference) < threshold


def funname(stackpos):
    """
    Returns the function name from the current call stack, unwinding `stackpos`
    entries. This function is at `stackpos` 0, its caller is at 1, etc.

    Args:
        stackpos: Call stack position.

    Returns:
        Stack frame function name.
    """
    return str(inspect.stack()[stackpos][3])


def funname_message(message):
    """
    Returns the name of the test function and the
    success/error message, which is the result of the test.

    E.g.: test_at_setspd_kl204_success:{'msg': '', 'success': 'Ok'}

    Args:
        message: E.g. {'msg': '', 'success': 'Ok'}
    """
    return funname(2) + ":" + str(message)


def printrecv(data, stackpos=2):
    """
    Prints the data received by test from bluesky.
    Also prints the calling test function, for context.
    Args:
        data: Received data.
    """
    print("-- {} --: Data received: {}".format(funname(stackpos), data))


def wait_for(test, iters=-1, period=1):
    """
    Performs up to `iters` iterations of a `test`, stopping when `test` is True.
    Employs an exponentially increasing wait time between test iterations.
    Args:
        test: The test to perform
        iters: The number of iterations of `test`.  -1 means indefinite.
        period: The initial wait period in seconds between test iterations.

    Returns:

    """
    if iters == 0:
        raise BlueSkyTestException()
    elif iters > 0:
        iters -= 1

    time.sleep(period)  # front-load a sleep

    try:
        result = test()
    except:
        result = False

    if result:
        return result
    return wait_for(test, iters, 2 * period)


class BlueSkyTestException(Exception):

    """
    Simple base exception class for bluesky tests.
    """
    pass

