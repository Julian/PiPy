from klein import Klein
from twisted.python.filepath import FilePath
from twisted.web.server import Site
from twisted.web.static import File

STATIC_DIR = FilePath(__file__).sibling("static")


class Pi(object):

    app = Klein()

    def site(self, displayTracebacks=True, **kwargs):
        """
        A :twisted:`web.server.Site` that will serve me.

        """

        site = Site(self.app.resource(), **kwargs)
        site.displayTracebacks = displayTracebacks
        return site

    @app.route("/")
    @app.route("/static", branch=True)
    def index(self, request):
        return File(STATIC_DIR.path)
