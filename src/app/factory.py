import os

from .base_class import App
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(app_name=__name__):
    app = App(app_name)

    app.connect_private_malclient_instance()
    app.data_bank.populate_top_rankings(app._private_client)
    app.connect_database()

    # Configure proxy:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1, x_prefix=1)

    from .base_paths import page_base_blueprint
    from .error_handlers import error_handler_blueprint
    from .recommendation_paths import recommendations_blueprint

    app.register_blueprint(page_base_blueprint)
    app.register_blueprint(error_handler_blueprint)
    app.register_blueprint(recommendations_blueprint)

    return app
