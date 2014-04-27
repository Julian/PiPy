from klein import Klein
from twisted.python.components import registerAdapter
from twisted.python.filepath import FilePath
from twisted.web.server import Session
from twisted.web.static import File
from zope.interface import Interface, Attribute, implementer

from pi.auth import Authenticator, AuthenticationError


STATIC_DIR = FilePath(__file__).sibling("static")


class Pi(object):

    app = Klein()

    def __init__(self, audience):
        self.authenticator = Authenticator(audience=audience)

    @app.route("/auth/login", methods=["POST"])
    def login(self, request):
        assertion = request.args.get("assertion")
        try:
            response = self.authenticator.authenticate(assertion=assertion)
        except AuthenticationError:
            request.setResponseCode(204)
            return
        else:
            response.addCallback(IPersona(request.getSession()).success)

    @app.route("/auth/logout", methods=["POST"])
    def logout(self, request):
        request.getSession().expire()

    @app.route("/auth/status")
    def status(self, request):
        email = IPersona(request.getSession()).email
        if email is not None:
            return email
        request.setResponseCode(401)

    @app.route("/")
    @app.route("/static", branch=True)
    def index(self, request):
        return File(STATIC_DIR.path)


class IPersona(Interface):
    email = Attribute("The e-mail of the logged in user.")

    def success(response):
        """
        A successful response was received from the authenticator.

        """


@implementer(IPersona)
class Persona(object):
    def __init__(self, session):
        self.email = None

    def success(self, response):
        self.email = response["email"]


registerAdapter(Persona, Session, IPersona)
