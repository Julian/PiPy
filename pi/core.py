from twisted.web import resource


class PiResource(resource.Resource):

    isLeaf = True

    def render_GET(self, request):
        return "<h2>Hello World!</h2>"
