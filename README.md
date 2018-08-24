# A Conversational UI Prototype

During our university masters seminar we build a chat bot prototype to enhance the user experience on the MOOC platform [Open SAP](https://open.sap.com/). In the following we will give a short overview over our experiment including how to train models and use the conversational UI prototype. 


## Table of contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Docker Services](#docker-services)
- [Training Models](#training-models)
- [Actions](#actions)
- [Future Work](#future-work)


## Introduction

[Rasa](https://rasa.com/) is an open source platform for building chat bots. It consists of two major parts: the Rasa Core and the Rasa NLU. On top of that we additionally build our own Chat UI frontend in ReactJS. 

![CUI Architecture](https://github.com/schul-cloud/cui/blob/feature/documentation/cui_Architecture.png)

### Rasa NLU
The Rasa NLU is responsible for the Natural Language Understanding of the chatbot. It receives an input (e.g. a sentence) from the user through the UI and predicts an intent of that sentence. The intent defines how the chatbot will react to a certain input. 

### Rasa Core
Rasa Core takes the output of the NLU (a structured input e.g. an intent) and decides on an action to perform on it. Actions can be several things: an API Call, a response in form of an utterance or just an input validation (read more [Actions](#actions)). These actions are send back to the frontend as the bots response. 


### Chat UI
The chat UI is a simple reactJS frontend. It consits of a simple input mask where the user can enter question or actions to the bot and communicate with it. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. You will train a model for both the dialogue engine and the NLU and send your first message to the bot. 

### Prerequisities

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

Service | Description | Port | URL
---|---|---|---
Chat UI | Demo to show the interface on the openSAP landing page. | 3000 | http://localhost:3000
Rasa Core | Rasa Core instance for a predefined project. | 5005 | http://localhost:5005/conversations/default/respond?q=hello
Rasa NLU | Rasa NLU instance, which can be used for multiple  projects. | 5000 | http://localhost:5000/parse?q=hello&project=opensap_faq
Rasa NLU Training | Runs a cron job, which starts the NLU training daily at midnight. | | 
Duckling | Entitiy extraction service for predefined entities. For more information see the [Rasa](https://rasa.com/docs/nlu/pipeline/#ner-duckling-http) and [duckling documentation](https://duckling.wit.ai/). | 8000 |


## Training Models

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

Actions are the things the bot can do. As described in the [Getting Started](#getting-started) section one action type are simple utterances, that can be defined in the domain of your project. Furthermore variables can be used in the templates to [fill them with slot entries](https://rasa.com/docs/core/slotfilling/). But you can also define your own custom actions with some Python code to call an API or do whatever you can think of.

Rasa provides a basic [`Action`](https://github.com/RasaHQ/rasa_core/blob/master/rasa_core/actions/action.py) class to inherit from and a more specific [`FormAction`](https://github.com/RasaHQ/rasa_core/blob/master/rasa_core/actions/forms.py). The latter one is a simplification for use cases, where you need a specific set of data values from the user to perform an action. You can find a small example in [`rasa-core/actions/opensap_faq/account.py`](rasa-core/actions/opensap_faq/account.py). The class `ActionEmailForm` gets an email address from the user and prompts him to confirm it. Only if these two steps are done, the `submit` function is called.

To use your custom actions in your stories they have to be added to your projects domain.

```yml
actions:
    - opensap_faq.account.ActionEmailForm
```


## Future Work
As already mentioned before this is just a prototype and there are some things that can be implemented in the future to introduce it as a beta feature. Two things we want to point out a bit more detailed:

1. Session Management
2. Authorization for Actions

### Session Management & Authorization
Session Management and Authorization for Actions come hand in hand. Session Management is an important feature for every online service especially chat bots and therefore every session should be time-boxed. At the end of each session the user needs to authorize once again. This is on the one hand an important aspect for the actions which the bot wants to perform. For example, in order to change the email-address of the user, the bots needs to have the permission to access the users settings. On the other hand, it is a necessary security feature to limit the bots access to certain commands and prevent unwanted actions.  

