from zope.interface import implementer

from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.web import server

from pi.core import Pi


class Options(usage.Options):
    optParameters = [
        ["audience", "The audience (domain) to use for Persona verification"],
        ["port", "p", "A strports port to run on"],
    ]


@implementer(IPlugin, IServiceMaker)
class PiServiceMaker(object):
    tapname = "pi"
    description = "Start the pi service."
    options = Options

    def makeService(self, options):
        from twisted.internet import reactor
        endpoint = serverFromString(reactor, options["port"])
        pi = Pi(audience=options["audience"])
        return StreamServerEndpointService(
            endpoint=endpoint, factory=server.Site(pi.app.resource()),
        )


serviceMaker = PiServiceMaker()
