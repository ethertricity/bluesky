"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.

Author <ahfarrell@sparkl.com> Andrew Farrell
Test configuration for scenario tests
"""
import os
from ..conftest import *


@pytest.fixture(scope="session")
def snaplog(pytestconfig):
    """
    Suite-level setup and teardown function, for those test functions
    naming `sock` in their parameter lists.
    """
    rootdir = str(pytestconfig.rootdir)
    outputdir = os.path.join(rootdir, 'output')
    yield outputdir
