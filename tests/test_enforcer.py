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
        (["panda"], True),
        (["panda", "other_role"], True),
    ],
)
def test_user_contact_read_access(authz, roles, expected):
    assert (
        authz.enforce(
            roles,
            "user_contact",
            "read",
            {},
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
            ["panda"],
            "task",
            "update",
            {
                "tasktype": "prod",
            },
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
            ["panda"],
            "task",
            "update",
            {
                "tasktype": "analy",
            },
            new,
        )
        is expected
    )


@pytest.mark.parametrize(
    "obj_type, obj, act",
    [
        ("task", {"tasktype": "prod"}, "read"),
        ("dataset", {}, "update"),
        ("user_contact", {}, "update"),
    ],
)
def test_wrong_object_or_action_denied(authz, obj_type, obj, act):
    assert (
        authz.enforce(
            ["panda"],
            obj_type,
            act,
            obj,
            {},
        )
        is False
    )
