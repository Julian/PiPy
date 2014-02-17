from zope.interface import implementer

from twisted.application import strports
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage
from twisted.web import server

from pi.core import PiResource


class Options(usage.Options):
    optParameters = [["port", "p", "A strports port to run on"]]


@implementer(IPlugin, IServiceMaker)
class PiServiceMaker(object):
    tapname = "pi"
    description = "Start the pi service."
    options = Options

    def makeService(self, options):
        return strports.service(options["port"], server.Site(PiResource()))


serviceMaker = PiServiceMaker()
