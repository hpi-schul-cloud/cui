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
    ```sh
    git clone git@github.com:schul-cloud/cui.git
    ```
1. Build the images by going to the root directory and execute the following command.
    ```sh
    docker-compose build
    ```
    This may take a while...
1. Train the models, so the chatbot knows how to behave.
    ```sh
    docker-compose run rasa-core python -m rasa_core.train -d data/opensap_faq/domain.yml -s data/opensap_faq/stories.md -o model/opensap_faq --epochs 200
    ```
    ```sh
    docker-compose run rasa-nlu python -m rasa_nlu.train -c config.yml -d data/opensap_faq -o projects --project opensap_faq
    ```
1. Start the containers.
    ```sh
    docker-compose up
    ```
1. Open [`http://localhost:3000`](http://localhost:3000) to access the chat interface. The first request to the bot may take a few moments, since the NLU has to be initialized.


### Add intent with simple utterance

1. Define examples of what the user might say to express the intent. This is done in the training data of the NLU in one or multiple Markdown files. These can be located in `rasa-nlu/data/<project-name>`.
    ```markdown
    ## intent:sound_of_cat
    - what does the cat say
    - what does a cat sound like
    ```
1. Now the dialogue engine might receive the `sound_of_cat` intent, which has to be added to its domain. Since the bot should only output a simple text response, its template can also be specified in `rasa-core/data/<project-name>/domain.yml`.
    ```yml
    intents:
        - sound_of_cat
    
    actions:
        - utter_sound_of_cat

    templates:
        utter_sound_of_cat:
            - text: Meow!
            - text: Meow meow!
    ```
    Since there are multiple templates defined, Rasa Core will choose one randomly.
1. Add training data for the conversational flow, so that the bot triggers the correct action `utter_sound_of_cat` after the intent `sound_of_cat`. This training data is located in `rasa-core/data/<project-name>/stories.md`.
    ```markdown
    ## Make meow sound <this line is just a comment>
    * sound_of_cat
        - utter_sound_of_cat
    ```
1. Train the models as described in [Training Models](#training-models).

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