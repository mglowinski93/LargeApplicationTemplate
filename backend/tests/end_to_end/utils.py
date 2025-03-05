from flask import Flask, url_for


def get_url(
    app: Flask,
    routes: dict,
    url_type: str,
    path_parameters: dict | None = None,
    query_parameters: dict | None = None,
) -> str:
    _path_parameters: dict = path_parameters or {}
    _query_parameters: dict = query_parameters or {}

    with app.app_context(), app.test_request_context():
        try:
            return url_for(routes[url_type], **_path_parameters, **_query_parameters)
        except KeyError:
            raise ValueError(f"Invalid type: {url_type}")
