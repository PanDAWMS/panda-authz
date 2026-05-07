# panda-authz

Reusable authorization library for PanDA WMS services built on top of PyCasbin.

`panda-authz` provides:

- A shared Casbin model
- Standard matcher functions
- File-based policy loading
- A simple `AuthorizationService` API
- Reusable authorization logic across multiple PanDA WMS components

---

## Installation

```bash
pip install panda-authz
````

## Quick Start

Create a policy file, more about the policy format in the [documentation](docs/policy-format.md):

```text
# policy.csv
p, panda, user_contact, read, {}, {}, allow
p, panda, task, update, {"tasktype": "prod"}, {"priority": [500, 999]}, allow
```

Create and use the authorization service:

```python
from panda_authz.service import AuthorizationService
authz = AuthorizationService("policy.csv")
allowed = authz.enforce(
    ["panda"],
    "user_contact",
    "read",
    {},
    {},
)

print(allowed)  # True
```

more examples in the [documentation](docs/examples.md).

### Django Integration

```python
# oauth/authz.py
from django.conf import settings
from panda_authz.service import AuthorizationService
authz = AuthorizationService(settings.AUTHZ_POLICY_FILE_PATH)
```

Then use it in views or service code:

```python
from oauth.authz import authz
if not authz.enforce(
    request.user_roles,
    "user_contact",
    "read",
    {},
    {},
):
    raise PermissionDenied()
```
