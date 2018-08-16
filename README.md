# A Conversational UI Experiment

_What is this experiment about?_

## Table of contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Docker Services](#docker-services)
- [Training Models](#training-models)
- [Actions](#actions)
- [Future Work](#future-work)


## Introduction

_[Theresa]_

_Short intro to Rasa and our Architecture_

### Rasa Core

### Rasa NLU

### Chat UI


## Getting Started

_[Felix]_

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. You will train a model for both the dialogue engine and the NLU and send your first message to the bot.

### Prerequisities

* Git
* Docker with Docker Compose


### Installation

1. Clone the repository.
    ```
    git clone git@github.com:schul-cloud/cui.git
    ```
1. Build the images by going to the root directory and execute the following command.
    ```
    docker-compose build
    ```
    This may take a while...
1. Train the models, so the chatbot knows how to behave.
    ```
    docker-compose run rasa-core python -m rasa_core.train -d data/opensap_faq/domain.yml -s data/opensap_faq/stories.md -o model/opensap_faq --epochs 200
    ```
    ```
    docker-compose run rasa-nlu python -m rasa_nlu.train -c config.yml -d data/opensap_faq -o projects --project opensap_faq
    ```
1. Start the containers.
    ```
    docker-compose up
    ```
1. Open [`http://localhost:3000`](http://localhost:3000) to access the chat interface. The first request to the bot may take a few moments, since the NLU has to be initialized.


## Docker Services

_[Felix]_

Service | Description | Port | URL
---|---|---|---
Chat UI | | 3000 | http://localhost:3000
Rasa Core | | 5005 | http://localhost:5005/conversations/default/respond?q=hello
Rasa NLU | | 5000 | http://localhost:5000/parse?q=hello&project=opensap_faq
Rasa NLU Training | | | 
Duckling | | 8000 |


## Training Models

_[Theresa]_

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

## Actions

_[Felix]_

_How do Action work? How are they implemented?_


## Future Work

_[Theresa]_

_What else is there to do?_