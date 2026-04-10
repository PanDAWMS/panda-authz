from pathlib import Path

import pytest

from panda_authz.service import AuthorizationService


@pytest.fixture(scope="module")
def authz():
    policy_file = Path(__file__).parent / "policy_test.csv"
    return AuthorizationService(str(policy_file))


def test_authorization_service_initializes(authz):
    assert authz is not None
    assert authz.enforcer is not None
