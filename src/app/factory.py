import os

from .base_class import App


def create_app(app_name=__name__):
    app = App(app_name)

    from .base_paths import page_base_blueprint
    from .error_handlers import error_handler_blueprint
    from .recommendation_paths import recommendations_blueprint

    app.register_blueprint(page_base_blueprint)
    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(recommendations_blueprint)

    return app
