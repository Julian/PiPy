from twisted.application import internet, strports
from twisted.application.service import MultiService
from twisted.python import usage
import twisted.names.cache
import twisted.names.client
import twisted.names.dns
import twisted.names.server

from pi.core import Pi


class Options(usage.Options):
    optParameters = [
        [
            "access-log",
            "l",
            None,
            "Path to web CLF (Combined Log Format) log file for access logs.",
        ],
        ["web", "W", "tcp:8080", "The endpoint to listen on for web."],
        ["dns", "D", 5333, "The port to listen on for DNS"],
    ]

    optFlags = [
        ["verbose", "v", "Log verbosely"],
    ]

    def postOptions(self):
        try:
            self["dns"] = int(self["dns"])
        except ValueError:
            raise usage.UsageError(
                "Invalid DNS port: {!r}".format(self["dns"]),
            )


def _makeServices(options):
    site = Pi().site(logPath=options["access-log"])
    yield strports.service(description=options["web"], factory=site)

    dnsServer = twisted.names.server.DNSServerFactory(
        authorities=[],
        caches=[
            twisted.names.cache.CacheResolver(verbose=options["verbose"]),
        ],
        clients=[
            twisted.names.client.createResolver(servers=options),
        ],
        verbose=options["verbose"],
    )
    yield internet.TCPServer(options["dns"], dnsServer)
    yield internet.UDPServer(
        options["dns"],
        twisted.names.dns.DNSDatagramProtocol(dnsServer),
    )


def makeService(options):
    service = MultiService()
    for each in _makeServices(options=options):
        each.setServiceParent(service)
    return service
