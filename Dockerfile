FROM python:3.11.2-buster

RUN pip install --upgrade pip
RUN apt-get update && apt-get install curl -y

RUN useradd flask_user
RUN mkdir /home/anime_suggester && chown flask_user:flask_user /home/anime_suggester
RUN mkdir -p /var/log/flask_server && touch /var/log/flask_server/flask_server.err.log && touch /var/log/flask_server/flask_server.out.log
RUN chown -R flask_user:flask_user /var/log/flask_server
WORKDIR /home/anime_suggester/

COPY --chown=flask_user:flask_user ./src .
#COPY ./src .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY ./build_files/run.sh ./run.sh
COPY ./build_files/celery/* ./celery_daemon/
RUN sh ./celery_daemon/make_celery.sh

EXPOSE 5000
#USER flask_user

# To jest security issue jak chuj, ale przynajmniej działa...
# celeryd must be started as privileged user
CMD ["sh", "./run.sh"]