from zope.interface import implementer

from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.web import server

from pi.core import app


class Options(usage.Options):
    optParameters = [["port", "p", "A strports port to run on"]]


@implementer(IPlugin, IServiceMaker)
class PiServiceMaker(object):
    tapname = "pi"
    description = "Start the pi service."
    options = Options

    def makeService(self, options):
        from twisted.internet import reactor
        return StreamServerEndpointService(
            endpoint=serverFromString(reactor, options["port"]),
            factory=server.Site(app.resource()),
        )


serviceMaker = PiServiceMaker()
