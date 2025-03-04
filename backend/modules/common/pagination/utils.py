import urllib.parse as urlparse
from urllib.parse import urlencode


def get_next_pagination_link(
    url: str, offset: int, records_per_page: int, all_records_count: int
) -> str | None:
    link = None
    if all_records_count - records_per_page > offset:
        # More about adding query params to url:
        # https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python.
        params = {"offset": offset + records_per_page}
        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)  # type: ignore
        url_parts[4] = urlencode(query)
        link = urlparse.urlunparse(url_parts)

    return link


def get_previous_pagination_link(
    url: str, offset: int, records_per_page: int
) -> str | None:
    link = None
    if offset != 0 and records_per_page >= offset:
        link = url.replace(f"offset={offset}", "").rstrip("&").rstrip("?")
    elif records_per_page - offset < 0:
        link = url.replace(f"offset={offset}", f"offset={offset-records_per_page}")

    return link
