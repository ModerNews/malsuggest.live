from app import create_app
from app import celery  # This seems to be unused, however celery instance and worker will be pointed here.
from werkzeug.middleware.proxy_fix import ProxyFix

if __name__ == "__main__":
    app = create_app(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1, x_prefix=1)
    app.run("0.0.0.0")