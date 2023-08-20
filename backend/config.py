import os


class Config:
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
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
    "title": "Diagrams API",
}
