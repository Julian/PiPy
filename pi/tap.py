from twisted.application.strports import service
from twisted.python import usage

from pi.core import Pi
from pi.utils import Redirect, argparseToOptions


class Options(usage.Options):
    optParameters = [
        [
            "access-log",
            "l",
            None,
            "Path to web CLF (Combined Log Format) log file for access logs.",
        ],
        ["port", "p", "tcp:8080", "The endpoint to listen on."],
    ]


def makeService(options):
    site = Pi().site(logPath=options["access-log"])
    return service(options["port"], site)
