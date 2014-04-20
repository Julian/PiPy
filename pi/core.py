import os

from klein import Klein
from twisted.web.static import File


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app = Klein()


@app.route("/", branch=True)
def static(request):
    return File(STATIC_DIR)
