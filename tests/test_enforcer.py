from pathlib import Path

import pytest

from panda_authz.service import AuthorizationService


@pytest.fixture(scope="module")
def authz():
    policy_file = Path(__file__).parent / "policy_test.csv"
    return AuthorizationService(str(policy_file))


@pytest.mark.parametrize(
    "roles, expected",
    [
        ([], False),
        (["some_role"], False),
        (["atlas-adc-pandamon"], True),
        (["atlas-adc-pandamon", "other_role"], True),
    ],
)
def test_user_contact_read_access(authz, roles, expected):
    assert (
        authz.enforce(
            roles,
            {"type": "user_contact"},
            "read",
            {},
        )
        is expected
    )


@pytest.mark.parametrize(
    "new, expected",
    [
        ({"priority": 500}, True),
        ({"priority": 750}, True),
        ({"priority": 999}, True),
        ({"priority": 499}, False),
        ({"priority": 1000}, False),
        ({}, False),
        ({"priority": "700"}, True),
    ],
)
def test_prod_task_priority_update(authz, new, expected):
    assert (
        authz.enforce(
            ["atlas-adc-pandamon"],
            {
                "type": "task",
                "tasktype": "prod",
            },
            "update",
            new,
        )
        is expected
    )


@pytest.mark.parametrize(
    "new, expected",
    [
        ({"globalshare": "Express Analysis"}, True),
        ({"globalshare": "User Analysis"}, True),
        ({"globalshare": "Production"}, False),
        ({"globalshare": "Unknown"}, False),
        ({}, False),
    ],
)
def test_analy_task_globalshare_update(authz, new, expected):
    assert (
        authz.enforce(
            ["atlas-adc-pandamon"],
            {
                "type": "task",
                "tasktype": "analy",
            },
            "update",
            new,
        )
        is expected
    )


@pytest.mark.parametrize(
    "obj, act",
    [
        ({"type": "task", "tasktype": "prod"}, "read"),
        ({"type": "dataset"}, "update"),
        ({"type": "user_contact"}, "update"),
    ],
)
def test_wrong_object_or_action_denied(authz, obj, act):
    assert (
        authz.enforce(
            ["atlas-adc-pandamon"],
            obj,
            act,
            {},
        )
        is False
    )
