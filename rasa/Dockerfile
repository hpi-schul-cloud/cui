FROM rasa/rasa:latest-full

COPY config.yml /app/config.yml
COPY domain.yml /app/domain.yml
COPY credentials.yml /app/credentials.yml
COPY endpoints.yml /app/endpoints.yml
COPY data/* /app/data/
COPY models/* /app/models/
COPY actions.py /app/actions.py

ENTRYPOINT ["rasa"]
