import casbin
from importlib.resources import files
from .functions import match_object, match_constraints, match_role


class AuthorizationService:
    def __init__(self, policy_path: str):
        model_path = str(files("panda_authz").joinpath("model.conf"))

        self.enforcer = casbin.Enforcer(model_path, policy_path)

        self.enforcer.add_function("match_role", match_role)
        self.enforcer.add_function("match_object", match_object)
        self.enforcer.add_function("match_constraints", match_constraints)

    def enforce(self, sub, obj, act, params=None):
        params = params or {}
        return self.enforcer.enforce(sub, obj, act, params)