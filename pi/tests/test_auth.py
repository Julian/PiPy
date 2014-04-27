from unittest import TestCase

from pi import auth


class TestAuthenticator(TestCase):
    def test_received_successful_response(self):
        response = {
            "status": "okay",
            "email": "bob@eyedee.me",
            "audience": "https://example.com:443",
            "expires": 1308859352261,
            "issuer": "eyedee.me"
        }
        self.assertEqual(
            auth.Authenticator(audience="")._received_response(response),
            response,
        )

    def test_received_unsuccessful_response(self):
        response = {
            "status": "failure",
            "reason": "Just because",
        }
        with self.assertRaises(auth.VerificationFailed) as e:
            auth.Authenticator(audience="")._received_response(response)
        self.assertEqual(str(e.exception), "Just because")

    def test_if_there_is_no_assertion_we_raise_an_exception(self):
        with self.assertRaises(auth.MissingAssertion):
            auth.Authenticator(audience="").authenticate(assertion=None)
