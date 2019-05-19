"""Test app utilities."""

from conduit.util import expandvars_dict


def test_expandvars_dict() -> None:
    """Test if config vars are properly parsed."""
    settings = {
        "really": "true",
        "count": "1",
        "url": "http://${HOST:-localhost}:${PORT:-8080}",
        "foo": "bar",
        "empty": "",
    }

    expanded = {
        "really": True,
        "count": 1,
        "url": "http://localhost:8080",
        "foo": "bar",
        "empty": None,
    }

    assert expandvars_dict(settings) == expanded
