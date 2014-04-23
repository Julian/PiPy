from klein import Klein
from twisted.python.filepath import FilePath
from twisted.python import log
from twisted.web.static import File


STATIC_DIR = FilePath(__file__).sibling("static")
app = Klein()


@app.route("/auth/login", methods=["POST"])
def login(request):
    assertion = request.args.get("assertion")
    if assertion is None:
        pass


@app.route("/auth/logout", methods=["POST"])
def logout(request):
    pass


@app.route("/")
@app.route("/static", branch=True)
def index(request):
    return File(STATIC_DIR.path)
