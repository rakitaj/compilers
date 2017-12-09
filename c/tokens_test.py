import pytest
from tokens import *

class TestTokens(object):

    def test_token_equality(self):
        token1 = Token("zip code", "[0-9]{5}", "90210")
        token2 = Token("zip code", "[0-9]{5}", "90210")
        assert token1 == token2
