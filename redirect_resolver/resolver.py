"""Resolves the HTTP(S) redirect."""

from urllib.parse import urlparse

import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10_10_1) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36"
    )
}


def resolve_redirect(url):
    """Resolves a redirect."""

    try:
        with requests.get(
            url, allow_redirects=False, stream=True, headers=HEADERS
        ) as response:
            redirect_url = response.headers.get("Location")
            return (
                urlparse(redirect_url).netloc if redirect_url else urlparse(url).netloc
            )
    except requests.exceptions.ConnectionError:
        return None
