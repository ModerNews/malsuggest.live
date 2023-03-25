from app import create_app
from app import celery  # This seems to be unused, however celery instance and worker will be pointed here.
from werkzeug.middleware.proxy_fix import ProxyFix

# Run this for production deployment only
if __name__ == "__main__":
    app = create_app(__name__)
    app.run("0.0.0.0")