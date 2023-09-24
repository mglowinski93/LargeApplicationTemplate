from flask import jsonify

from bootstrap import create_app
from modules.common import consts, docstrings


app = create_app()


@app.route("/health-check", strict_slashes=False)
@docstrings.inject_parameter_info_doc_strings(consts.SWAGGER_FILES)
def health_check():
    """
    file: {0}/health_check_endpoint.yml
    """

    return jsonify(
        {
            "health": "Running",
        }
    )
