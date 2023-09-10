class Config:
    SWAGGER_ENABLED = False
    LOG_LEVEL = "INFO"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SWAGGER_ENABLED = True
    LOG_LEVEL = "DEBUG"

    @staticmethod
    def init_app(app):
        pass


class TestConfig(Config):
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
