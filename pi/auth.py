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
    pass
