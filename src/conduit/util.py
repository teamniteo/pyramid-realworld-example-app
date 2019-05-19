"""Utilities for conduit app."""

from ast import literal_eval
from expandvars import expandvars

import typing as t


def safe_eval(text: str) -> t.Any:
    """Safely evaluate `text` argument.

    `text` can be evaluated to string, number,
    tuple, list, dict, boolean, and None.
    Code `text[0].upper() + text[1:]` is for lower case
    'false' or 'true' strings, it should not break anything.
    """
    if len(text) == 0:
        return None

    try:
        return literal_eval(text[0].upper() + text[1:])
    except (ValueError, SyntaxError):
        return text


def expandvars_dict(settings: t.Dict[str, str]) -> t.Dict[str, t.Any]:
    """Expand strings or variables from the environment into equivalent python literals or strings.

    >>> expandvars_dict({
    ...     "really": "true",
    ...     "count": "1",
    ...     "url": "http://${HOST:-localhost}:${PORT:-8080}"
    ... })
    {'really': True, 'count': 1, 'url': 'http://localhost:8080'}
    """
    return {key: safe_eval(expandvars(value)) for key, value in settings.items()}
