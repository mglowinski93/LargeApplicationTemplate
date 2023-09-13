from flask import jsonify

from bootstrap import create_app


app = create_app()


@app.route("/health-check", strict_slashes=False)
def health_check():
    """
    file: ./swagger_files/health_check_endpoint.yml
    """

    return jsonify(
        {
            "health": "Running",
        }
    )
