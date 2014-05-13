import argparse

from zope.interface import implementer

from twisted.application.internet import StreamServerEndpointService
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.application.service import IServiceMaker, MultiService
from twisted.plugin import IPlugin
from twisted.web import server

from pi.core import Pi
from pi.utils import Redirect, argparseToOptions


parser = argparse.ArgumentParser()
parser.add_argument(
    "--canonical-url",
    help="The public facing URL that should be used for the Persona audience "
         "and for any redirects.",
)
parser.add_argument(
    "--port", "-p",
    dest="endpoint",
    help="A strports port to run on",
    type=lambda strport : serverFromString(reactor, strport),
)

parser.add_argument(
    "--redirect", "-r",
    action="append",
    dest="redirects",
    type=lambda strport : serverFromString(reactor, strport),
    help="An endpoint to HTTP 301 redirect to the main port "
         "specified with --port. May be specified multiple times.",
)


@implementer(IPlugin, IServiceMaker)
class PiServiceMaker(object):
    tapname = "pi"
    description = "Start the pi service."
    options = argparseToOptions(parser)

    def makeService(self, options):
        pi = Pi(audience=options["canonical_url"])
        piService = StreamServerEndpointService(
            endpoint=options["endpoint"],
            factory=server.Site(pi.app.resource()),
        )

        redirects = options["redirects"]
        if not redirects:
            return piService

        service = MultiService()
        piService.setServiceParent(service)

        for redirect in redirects:
            redirectService = StreamServerEndpointService(
                endpoint=redirect,
                factory=server.Site(Redirect(options["canonical_url"])),
            )
            redirectService.setServiceParent(service)

        return service


serviceMaker = PiServiceMaker()
