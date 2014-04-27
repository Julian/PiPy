import treq


class AuthenticationError(Exception):
    pass


class VerificationFailed(AuthenticationError):
    """
    The verifier reported that the assertion was invalid.

    """


class MissingAssertion(AuthenticationError):
    """
    An attempted Persona authentication was missing the assertion.

    """


class Authenticator(object):
    """
    A Persona authenticator.

    """

    def __init__(
        self, audience, verifier="https://verifier.login.persona.org/verify",
    ):
        self.audience = audience
        self.verifier = verifier

    def authenticate(self, assertion):
        """
        Try to authenticate the given assertion with the verifier.

        """

        if assertion is None:
            raise MissingAssertion()
        return treq.post(
            self.verifier,
            data=dict(assertion=assertion, audience=self.audience),
        ).addCallback(treq.json_content).addCallback(self._received_response)

    def _received_response(self, response):
        status = response.get("status")
        if status == "okay":
            return response
        raise VerificationFailed(response.get("reason", ""))
