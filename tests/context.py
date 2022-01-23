import os
import pathlib
import sys

sys.path.insert(0,
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sozlukgetir


def _abspath(localpath):
    return pathlib.Path(__file__).parent.resolve()/localpath

def _url(localpath):
    return (_abspath(localpath).as_uri())
