export $(grep -v '^#' .env | xargs -d ';')
source venv/bin/activate

sudo docker start test-redis

celery -A runner.celery flower & disown
celery -A runner.celery worker -l info --pool=solo & disown

python runner.py