from locust import task

from tests.performance.entrypoints.template_app.base import BaseApiTests


class TemplateApiTests(BaseApiTests):
    @task
    def list_templates(self):
        self.client.get(
            "/api/templates/",
        )

    @task
    def get_template(self):
        self.client.get(
            f"/api/templates/{self.template_id}",
        )
