from locust import events

from tests.performance.base import BaseSetup


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--template-id",
        type=str,
        env_var="template_id",
        required=True,
        help="ID of template instance to use for performance retrieve method test",
    )


class BaseApiTests(BaseSetup):
    abstract = True

    def on_start(self):
        self.template_id = self.environment.parsed_options.template_id
