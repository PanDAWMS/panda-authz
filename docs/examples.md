## Examples

### Example 1: Read Access

Policy:

```text
p, atlas-adc-pandamon, user_contact, read, {}, {}, allow
```

Code:

```python
assert authz.enforce(
    ["panda"],
    "user_contact"
    "read",
    {},
    {},
)
```

### Example 2: Restrict Task Updates by Task Type

Policy:

```text
p, atlas-adc-pandamon, task, update, {"tasktype": "prod"}, {"priority": [500,999]}, allow
```

Allowed:

```python
authz.enforce(
    ["panda"],
    "task",
    "update",
    {
        "tasktype": "prod",
    },
    {
        "priority": 700,
    },
)
# True
```

Denied:

```python
authz.enforce(
    ["panda"],
    "task",
    "update",
    {
        "tasktype": "prod",
    },
    {
        "priority": 1000,
    },
)
# False
```

### Example 3: Restrict Analysis Shares

Policy:

```text
p, atlas-adc-pandamon, task, update, {"tasktype": "analy"}, {"globalshare": ["Express Analysis", "User Analysis"]}, allow
```

```python
authz.enforce(
    ["panda"],
    "task",
    "update",
    {
        "tasktype": "analy",
    },
    {
        "globalshare": "Express Analysis",
    },
)
# True
```