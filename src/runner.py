from app import create_app, socketio

from app import celery


if __name__ == "__main__":
    app = create_app(celery, app_name=__name__)
    socketio.run(app, "0.0.0.0", allow_unsafe_werkzeug=True)