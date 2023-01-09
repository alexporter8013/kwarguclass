from functools import wraps
from dataclasses import dataclass
import inspect
from .error import KwargumentEnableError


def kwarguclass_enable(fun):
    fun_sig = inspect.signature(fun)
    valid_params = list(filter(lambda n: n.lower().startswith("kwarg"), fun_sig.parameters))
    if len(valid_params) != 1:
        raise KwargumentEnableError("Must have one argument with name kwarg[s]")
    target_param_name = valid_params[0]
    target_param = fun_sig.parameters[target_param_name]
    target_kwclass = target_param.annotation
    if target_kwclass is None or not isinstance(target_kwclass, type):
        raise KwargumentEnableError("kwarg must be annotated with a class")
    target_kwclass_sig = inspect.signature(target_kwclass)
    bad_kwclass_params = []
    for param in target_kwclass_sig.parameters.values():
        valid = (
            param.kind == param.KEYWORD_ONLY
            or param.kind == param.POSITIONAL_OR_KEYWORD
        )
        if not valid:
            bad_kwclass_params.append(param)
    if len(bad_kwclass_params) > 0:
        raise KwargumentEnableError("Target kwarg class must be able to accept all arguments as keywords")
    for param in target_kwclass_sig.parameters.values():
        valid = (
            param.default != param.empty
        )
        if not valid:
            bad_kwclass_params.append(param)
    if len(bad_kwclass_params) > 0:
        raise KwargumentEnableError("Target kwarg class arguments must have default values")

    @wraps(fun)
    def enabled_version(*args, **kwargs):
        kwarg_value = target_kwclass(**kwargs)
        passed_in_dict = {target_param_name: kwarg_value}
        return fun(*args, **passed_in_dict)

    return enabled_version


kwarguclass = dataclass(kw_only=True, slots=True)
