## Authorization Request Format

The `enforce()` method takes four arguments:

```python
authz.enforce(roles, obj, act, params)
```

| Argument | Type        | Description                    |
|----------| ----------- | ------------------------------ |
| `roles`  | `list[str]` | Roles assigned to the user     |
| `obj`    | `dict`      | Existing object being accessed |
| `act`    | `str`       | Action being performed         |
| `params` | `dict`      | Requested modifications        |

Example:

```python
authz.enforce(
    ["atlas-adc-pandamon"],
    {
        "type": "task",
        "tasktype": "prod",
    },
    "update",
    {
        "priority": 700,
    },
)
```

---

## Policy Format

Policy rows follow this format:

```text
p, role, obj_type, act, obj_constraints, act_constraints, effect
```

Example:

```text
p, atlas-adc-pandamon, task, update, {"tasktype": "prod"}, {"priority": [500,999]}, allow
```

This means:

* role: `atlas-adc-pandamon`
* object type: `task`
* action: `update`
* applies only when `tasktype == "prod"`
* allows only priority changes between 500 and 999

---

## Casbin Model

The package ships with the following model:

```ini
[request_definition]
r = roles, obj, act, new

[policy_definition]
p = role, obj_type, act, obj_constraints, act_constraints, eft

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = r.obj.type == p.obj_type && \
    r.act == p.act && \
    match_role(r.roles, p.role) && \
    match_object(r.obj, p.obj_constraints) && \
    match_constraints(r.new, p.act_constraints)
```

