import os

from twisted.web import static


def create_resource():
    return static.File(
        os.path.join(os.path.dirname(__file__), "static"),
    )
