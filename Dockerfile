FROM python:3.11.2-alpine as base

RUN pip install --upgrade pip
RUN apk add curl
RUN apk add postgresql-libs 

RUN adduser -D flask_user
RUN mkdir /home/anime_suggester && chown flask_user:flask_user /home/anime_suggester
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R flask_user:flask_user /var/log/flask-app
WORKDIR /home/anime_suggester

COPY --chown=flask_user:flask_user ./src .

ENV FLASK_APP=runner.py
RUN \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 5000
USER flask_user

ENV CELERY_BROKER_URL=redis://192.168.0.21:6379/0
ENV CELERY_RESULT_BACKEND=redis://192.168.0.21:6379/1
ENV DB_HOST=192.168.0.21
ENV DB_PASS=
ENV DB_PORT=5432
ENV DB_SCHEMA=anime_suggester
ENV DB_USER=gruzin
ENV MAL_CLIENT_ID=48563b906310d3fdb4cefa1c1877bfc3
ENV MAL_CLIENT_SECRET=7d1c1c9dff161b5bf61dbbb1cc8ceed03d7988db888fc702ef8b9a6ebff7de7e 

CMD ["python", "runner.py"]