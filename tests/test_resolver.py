"""Tests resolver.py."""

from redirect_resolver.resolver import resolve_redirect


def test_resolve_redirect_on_redirector():
    """Tests resolve_redirect on a URL that is known to redirect."""
    result = resolve_redirect("http://www.gogle.com")
    assert result == "www.google.com"


def test_resolve_redirect_on_bad_url():
    """Tests resolve_redirect on a URL that doesn't resolve."""
    result = resolve_redirect("http://www.thisdomaindoesntresolve.com")
    assert result is None


def test_resolve_redirect_on_non_redirector():
    """Tests resolve_redirect on a URL that resolves, but does not redirect."""
    result = resolve_redirect("http://www.google.com")
    assert result == "www.google.com"
