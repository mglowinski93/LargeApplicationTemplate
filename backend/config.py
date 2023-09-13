import os


class Config:
    SWAGGER_ENABLED = False
    LOG_LEVEL = "INFO"

    DATABASE_USER = os.environ["POSTGRES_DB_USER"]
    DATABASE_PASSWORD = os.environ["POSTGRES_DB_PASSWORD"]
    DATABASE_HOST = os.environ["POSTGRES_DB_HOST"]
    DATABASE_PORT = os.environ["POSTGRES_DB_PORT"]
    DATABASE_NAME = os.environ["POSTGRES_DB_NAME"]

    @staticmethod
    def init_app(app):
        pass

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}"
            f"/{self.DATABASE_NAME}"
        )


class DevelopmentConfig(Config):
    SWAGGER_ENABLED = True
    LOG_LEVEL = "DEBUG"

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
    DATABASE_NAME = f"{Config.DATABASE_NAME}_test"

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig,
}


swagger_template = {
    "info": {
        "title": "LargeApplicationTemplate API",
        "description": "API description for large application template",
        "contact": {
            "responsibleDeveloper": "Mateusz Glowinski",
            "email": "mglowinski93@gmail.com",
            "url": "www.mateuszglowinski.pl",
        },
    },
    "schemes": ["http", "https"],
}


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "APISpecification",
            "route": "/spec",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "specs_route": "/swagger/",
    "url_prefix": "/api",
    "title": "LargeApplicationTemplate API",
}
