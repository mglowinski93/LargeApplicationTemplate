from locust import HttpUser, between


class BaseSetup(HttpUser):
    wait_time = between(1, 3)
    abstract = True
