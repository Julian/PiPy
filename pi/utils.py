from twisted.web.resource import Resource


class Redirect(Resource):

    isLeaf = True

    def __init__(self, url, code=301):
        Resource.__init__(self)
        self.code = code
        self.url = url

    def render(self, request):
        request.setHeader("Content-Type", "text/html; charset=utf-8")
        request.setResponseCode(self.code)
        request.setHeader(b"Location", self.url)
        return ""

    def getChild(self, name, request):
        return self


def argparseToOptions(parser):
    """
    Construct an L{IArgumentParser} out of an L{argparse.ArgumentParser}.

    @type parser: L{argparse.ArgumentParser}
    @param parser: an argument parser
    @return: an implementer of L{IArgumentPArser}

    See https://tm.tl/7330, hopefully this makes it into Twisted 14.1.

    """

    class _WrappedParser(object):
        def __init__(self):
            self._parsed = {}

        def __getitem__(self, option):
            return self._parsed[option]

        def parseOptions(self, options=None):
            """
            Parse the given options, storing the result.

            @type options: a L{list} of L{str}, or C{None}
            @param options: the options to parse
            """
            self._parsed = vars(parser.parse_args(args=options))

    return _WrappedParser
