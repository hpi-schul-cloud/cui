# A Conversational UI experiment


## How to run

```
docker-compose up --build
```


## Training

To train the respective service run one of the following commands from the root directory.

### Rasa Core

```
docker-compose run rasa-core python -m rasa_core.train \
    -d data/opensap_faq/domain.yml \
    -s data/opensap_faq/stories.md \
    -o model/opensap_faq \
    --epochs 200
```

### Rasa NLU
 
```
docker-compose run rasa-nlu python -m rasa_nlu.train \
    -c config.yml \
    -d data/opensap_faq \
    -o projects \
    --project opensap_faq
```


## Ports

Service | Port | URL
---|---|---
Rasa UI | 5001 | http://localhost:5001
Rasa NLU | 5000 | http://localhost:5000/parse?q=hello&project=opensap_faq
Rasa Core | 5005 | http://localhost:5005/conversations/default/respond?q=hello
