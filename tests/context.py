import os
import pathlib
import sys

sys.path.insert(0,
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sozlukgetir


def _url(localpath):
    return (pathlib.Path(__file__).parent.resolve()/localpath).as_uri()
