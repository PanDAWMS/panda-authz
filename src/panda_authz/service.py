from importlib.resources import as_file, files

import casbin

from .functions import match_constraints, match_object, match_role


class AuthorizationService:
    """Service for handling authorization using Casbin enforcer with custom functions."""

    def __init__(self, policy_path: str):
        """
        Initialize the AuthorizationService with a policy file.

        Args:
            policy_path (str): Path to the policy CSV file.
        """
        model_ref = files("panda_authz").joinpath("model.conf")
        try:
            with as_file(model_ref) as model_path:
                self.enforcer = casbin.Enforcer(str(model_path), policy_path)
                self.enforcer.add_function("match_role", match_role)
                self.enforcer.add_function("match_object", match_object)
                self.enforcer.add_function("match_constraints", match_constraints)
        except Exception as e:
            raise RuntimeError("Failed to init AuthorizationService") from e

    def enforce(
        self,
        roles: list[str],
        obj_type: str,
        act: str,
        obj: dict | None = None,
        params: dict | None = None,
    ) -> bool:
        """
        Enforce authorization for subject with list of roles, object, and action with optional parameters.

        Args:
            roles (list[str]): The roles of the subject (user) requesting access.
            obj_type (str): The object (resource) being accessed.
            act (str): The action being performed.
            obj (dict, optional): The object attributes for ABAC checks. Defaults to None.
            params (dict, optional): Additional parameters for enforcement. Defaults to None.

        Returns:
            bool: True if access is granted, False otherwise.
        """
        obj = obj or {}
        params = params or {}
        return self.enforcer.enforce(roles, obj_type, act, obj, params)
