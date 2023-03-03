from app import create_app

from app import celery


if __name__ == "__main__":
    app = create_app(celery, app_name=__name__)
    app.run("0.0.0.0", allow_unsafe_werkzeug=True)