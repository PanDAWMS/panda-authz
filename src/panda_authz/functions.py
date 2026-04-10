import json


def match_object(obj: dict, constraints: str) -> bool:
    """
    Checks if the object matches the given constraints.

    Args:
        obj (dict): The object to check against constraints.
        constraints (str): A JSON string representing the constraints.

    Returns:
        bool: True if the object matches the constraints, False otherwise.
    """
    if not constraints or constraints == "{}":
        return True

    constraint_dict = json.loads(constraints)
    return constraint_dict.items() <= obj.items()


def match_role(user_roles: list[str], policy_role: str) -> bool:
    """
    Checks if the policy role is in the user's roles.

    Args:
        user_roles (list[str]): List of roles assigned to the user.
        policy_role (str): The role required by the policy.

    Returns:
        bool: True if the policy role is in user roles, False otherwise.
    """
    return policy_role in user_roles


def match_constraints(params: dict, constraints: str) -> bool:
    """
    Checks if the new object params matches the constraints.

    Args:
        params (dict): The new object params to check.
        constraints (str): A JSON string representing the constraints.

    Returns:
        bool: True if matches, False otherwise.
    """
    if not constraints or constraints == "{}":
        return True

    constraint_dict = json.loads(constraints)

    for k, v in constraint_dict.items():
        if isinstance(v, list) and len(v) == 2 and all(isinstance(i, (int, float)) for i in v):
            val_min, val_max = v
            val_new = params.get(k)
            if val_new is None:
                return False
            try:
                val_new = int(val_new)
            except ValueError:
                raise
            if val_min <= val_new <= val_max:
                return True
        elif isinstance(v, list) and all(isinstance(i, str) for i in v):
            val_new = params.get(k)
            if val_new is None:
                return False
            if val_new in v:
                return True
    return False