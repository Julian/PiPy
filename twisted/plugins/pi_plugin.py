import argparse

from zope.interface import implementer

from twisted.application.internet import StreamServerEndpointService
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.web import server

from pi.core import Pi


parser = argparse.ArgumentParser()
parser.add_argument(
    "--audience",
    help="The audience (domain) to use for Persona verification",
)
parser.add_argument(
    "--port", "-p",
    help="A strports port to run on",
    type=lambda strport : serverFromString(reactor, strport),
)


def argparseToOptions(parser):
    """
    Construct an L{IArgumentParser} out of an L{argparse.ArgumentParser}.

    @type parser: L{argparse.ArgumentParser}
    @param parser: an argument parser
    @return: an implementer of L{IArgumentPArser}

    See https://tm.tl/7330, hopefully this makes it into Twisted 14.1.

    """

    class _WrappedParser(object):
        def __init__(self):
            self._parsed = {}

        def __getitem__(self, option):
            return self._parsed[option]

        def parseOptions(self, options=None):
            """
            Parse the given options, storing the result.

            @type options: a L{list} of L{str}, or C{None}
            @param options: the options to parse
            """
            self._parsed = vars(parser.parse_args(args=options))

    return _WrappedParser


@implementer(IPlugin, IServiceMaker)
class PiServiceMaker(object):
    tapname = "pi"
    description = "Start the pi service."
    options = argparseToOptions(parser)

    def makeService(self, options):
        pi = Pi(audience=options["audience"])
        return StreamServerEndpointService(
            endpoint=options["port"], factory=server.Site(pi.app.resource()),
        )


serviceMaker = PiServiceMaker()
