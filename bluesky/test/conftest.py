"""
Copyright (c) 2017 SPARKL Limited. All Rights Reserved.

Author <ahfarrell@sparkl.com> Andrew Farrell
Common test fixtures.
"""
import subprocess
import socket
import threading
import signal
import psutil
import pytest
from time import sleep
from . import wait_for, printrecv
from bluesky.tools.network import as_bytes

BLUESKY = "BlueSky_qtgl.py"
BUFFER_SIZE = 1024
TCP_HOST = "127.0.0.1"
TCP_PORT = 8888


def sock_connect(socket_, host, port):
    """
    Attempts a socket connection, and returns success boolean.

    Args:
        socket_: the socket, created with 'socket' method
        host:: the host
        port: the port

    Returns:
        whether socket is connected
    """
    try:
        socket_.connect((host, port))
        return True
    except ConnectionRefusedError:
        return False


def sock_send(socket_, msg):
    """
        Sends data across socket.
    """
    socket_.send(
        as_bytes(msg + "\n"))


def sock_receive(socket_):
    """
        Gets data from socket.
    """
    data = bytes(socket_.recv(BUFFER_SIZE)).decode('utf8').rstrip()
    printrecv(data)
    return data


def reset(sock_):
    """
    Resets running BlueSky
    """
    sock_send(sock_, "RESET")


def get_bluesky():
    """
    Gets running BlueSky processes
    :return: list of running processes
    """
    p = subprocess.Popen(
        "pgrep -f 'BlueSky(.py|_qtgl.py)'", stdout=subprocess.PIPE, shell=True)
    plist, _ = p.communicate()
    plist = list(set(plist.decode('utf8').split('\n')))
    popenpid = str(p.pid)
    if popenpid in plist:
        plist.remove(popenpid)
    plist.remove('')
    return plist


def start_bluesky(rootdir):
    """
    Starts BlueSky with python3
    """
    print("Starting BlueSky.")
    subprocess.call(
        'TESTING=false python3 {}'.format(BLUESKY), shell=True, cwd=rootdir)


def stop_bluesky():
    """
    Stops running BlueSky processes (called only if we started BlueSky)
    """
    print("Stopping BlueSky.")
    for p in get_bluesky():
        proc = psutil.Process(int(p))
        try:
            proc.send_signal(signal.SIGKILL)
        except psutil.NoSuchProcess:
            pass


@pytest.fixture(scope="session")
def sock(pytestconfig):
    """
    Suite-level setup and teardown function, for those test functions
    naming `sock` in their parameter lists.
    """
    rootdir = str(pytestconfig.rootdir)
    plist = get_bluesky()

    if not plist:
        # no running BlueSky
        server_thread = threading.Thread(
            target=lambda: start_bluesky(rootdir))
        server_thread.daemon = True
        server_thread.start()
        sleep(10)  # front-load a sleep before trying to connect

    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wait_for(
        lambda: sock_connect(sock_, TCP_HOST, TCP_PORT), -1, 5)

    yield sock_

    if plist:
        reset(sock_)
        sock_.close()
    else:
        stop_bluesky()
