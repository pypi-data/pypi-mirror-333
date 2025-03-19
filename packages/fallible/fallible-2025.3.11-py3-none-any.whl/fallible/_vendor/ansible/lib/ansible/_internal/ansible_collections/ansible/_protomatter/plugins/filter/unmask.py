from __future__ import annotations

import copy
import typing as t

from ansible._internal._templating._lazy_containers import _AnsibleLazyTemplateMixin
from ansible._internal._templating._engine import TemplateOptions


# DTFIX-MERGE: Ensure Galaxy CLI doesn't show warnings for this collection (eg, does not have a MANIFEST.json file, nor has it galaxy.yml)
def unmask(value: object, type_names: str | list[str]) -> object:
    """
    Internal filter to suppress automatic type transformation in Jinja (e.g., WarningMessageDetail, DeprecationMessageDetail, ErrorDetail).
    Lazy collection caching is in play- the first attempt to access a value in a given lazy container must be with unmasking in place, or the transformed value
    will already be cached.
    """
    if isinstance(type_names, str):
        type_names = [type_names]

    # DTFIX-MERGE: validation

    result: object

    if isinstance(value, _AnsibleLazyTemplateMixin):
        result = copy.copy(value)
        result._template_options = TemplateOptions(unmask_type_names=frozenset(type_names))
    else:
        result = value

    return result


class FilterModule(object):
    @staticmethod
    def filters() -> dict[str, t.Callable]:
        return dict(unmask=unmask)
