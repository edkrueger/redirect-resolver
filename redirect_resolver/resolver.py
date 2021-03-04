"""Resolves the HTTP(S) redirect."""

# pylint: disable=too-many-locals

import csv
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


def resolve_redirect(url, timeout=None):
    """Resolves a redirect."""

    try:
        with requests.get(
            url, allow_redirects=False, stream=True, headers=HEADERS, timeout=timeout
        ) as response:
            redirect_url = response.headers.get("Location")
            return (
                urlparse(redirect_url).netloc if redirect_url else urlparse(url).netloc
            )
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        return None


def redirect_resolver(in_path, out_path, in_column, out_column, timeout=None):
    """Redirect resolver."""
    with open(in_path, "r") as in_file, open(out_path, "w+") as out_file:
        dict_reader = csv.DictReader(in_file)
        in_fieldnames = dict_reader.fieldnames
        out_fieldnames = [*in_fieldnames, out_column]
        dict_writer = csv.DictWriter(out_file, fieldnames=out_fieldnames)
        dict_writer.writeheader()

        for in_row in dict_reader:
            in_url = in_row[in_column]
            url = "http://" + in_url if in_url else None
            resolved_url = resolve_redirect(url, timeout) if url else None
            out_row = {**in_row, out_column: resolved_url}
            dict_writer.writerow(out_row)


if __name__ == "__main__":
    redirect_resolver(
        "data/company_domain_list_filtered_100.csv",
        "redirected_company_domain_list.csv",
        "Company Domain Name",
        "Redirected URL",
        timeout=6,
    )
