# A Conversational UI Prototype

During our university masters seminar we build a chat bot prototype to enhance the user experience for pupils, teachers and parents when using [Schul-Cloud](https://schul-cloud.org/). In the following we will give a short overview over our experiment including how to train models and use the conversational UI prototype. 


## Table of contents
- [Introduction](#introduction)
- [Architecture](#architecture) 
- [Getting Started](#getting-started)
- [Docker Services](#docker-services)
- [Training Models](#training-models)
- [Actions](#actions)
- [Conclusion & Reflection](#conclusion-&-reflection)


## Introduction

Chatbots are text-based and automated dialogue systems, that allow to communicate with a computer-based system in natural language. They are divided into three categories. Support chatbots are specialized to answer questions from a specific domain. Skills chatbots have a predefined set of rules, e.g. to control the lights in your home. And assistant chatbots are a combination of support and skills chatbots. Alexa or Siri are two of the most popular ones.

Recent years have shown a rise in chatbots on the internet. Reason for this are not only the advancements in machine learning, but also how relatively easy it has become to build a chatbot with services like Dialogflow, Wit.ai or Microsoft’s Bot Framework. Often previous knowledge in machine learning is not required. Machine learning also allows for more complex chatbots. Although it is possible to build a chatbot with only a set of rules manifested in if-else-statements, at a certain point it is not feasible to maintain. Machine learning solves this by training a model from a set of example utterances and dialogues which evolves over time.

## Architecture

[Rasa](https://rasa.com/) is an open source platform for building chat bots. It consists of two major parts: the Rasa Core and the Rasa NLU. On top of that we additionally build our own Chat UI frontend in ReactJS. 

![CUI Architecture](https://raw.githubusercontent.com/schul-cloud/cui/master/cui_Architecture.png)

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
1. Adjust the project-names in  docker-compose.yml (line 10-14).
   ```sh
    # command: python -m rasa_core.server --debug -d model/*PROJECT-NAME*
    environment:
      - RASA_CORE_MODEL_PATH=./model/*PROJECT-NAME*
      - RASA_CORE_QUESTIONS_PATH=./data/*PROJECT-NAME*/intent_questions.json
      - RASA_NLU_PROJECT_NAME=*PROJECT-NAME*
    ```
1. Build the images by going to the root directory and execute the following command.
    ```sh
    docker-compose build
    ```
    This may take a while...
1. Train the models, so the chatbot knows how to behave.

    For Schul_cloud: 
    ```sh
    docker-compose run rasa-core python -m rasa_core.train -d data/schul_cloud/domain.yml -s data/schul_cloud/stories.md -o model/schul_cloud --epochs 200
    ```
    ```sh
    docker-compose run rasa-nlu python -m rasa_nlu.train -c config.yml -d data/schul_cloud -o projects --project schul_cloud
    ```

1. Start the containers.
    ```sh
    docker-compose up
    ```
1. Open [`http://localhost:3000`](http://localhost:3000) to access the chat interface. The first request to the bot may take a few moments, since the NLU has to be initialized.


## Docker Services

Service | Description | Port | URL
---|---|---|---
Chat UI | Demo to show the interface on the schul-cloud landing page. | 3000 | http://localhost:3000
Rasa Core | Rasa Core instance for a predefined project. | 5005 | http://localhost:5005/conversations/default/respond?q=hello
Rasa NLU | Rasa NLU instance, which can be used for multiple  projects. | 5000 | http://localhost:5000/parse?q=hello&project=schul_cloud
Rasa NLU Training | Runs a cron job, which starts the NLU training daily at midnight. | | 
Duckling | Entitiy extraction service for predefined entities. For more information see the [Rasa](https://rasa.com/docs/nlu/pipeline/#ner-duckling-http) and [duckling documentation](https://duckling.wit.ai/). | 8000 |


## Training Models

To train the respective service run one of the following commands from the root directory.

### Rasa NLU
 
```
docker-compose run rasa-nlu python -m rasa_nlu.train \
    -c config.yml \
    -d data/schul_cloud \
    -o projects \
    --project schul_cloud
```

### Rasa Core

```
docker-compose run rasa-core python -m rasa_core.train \
    -d data/schul_cloud/domain.yml \
    -s data/schul_cloud/stories.md \
    -o model/schul_cloud \
    --epochs 200
```

## Actions

Actions are the things the bot can do. As described in the [Getting Started](#getting-started) section one action type are simple utterances, that can be defined in the domain of your project. Furthermore variables can be used in the templates to [fill them with slot entries](https://rasa.com/docs/core/slotfilling/). But you can also define your own custom actions with some Python code to call an API or do whatever you can think of.

Rasa provides a basic [`Action`](https://github.com/RasaHQ/rasa_core/blob/master/rasa_core/actions/action.py) class to inherit from and a more specific [`FormAction`](https://github.com/RasaHQ/rasa_core/blob/master/rasa_core/actions/forms.py). The latter one is a simplification for use cases, where you need a specific set of data values from the user to perform an action. You can find a small example in [`rasa-core/actions/schul_cloud/first-lesson.py`](rasa-core/actions/schul_cloud/first-lesson.py). The class `GetFirstLesson` calls the schul_cloud API /calender endpoint and then filters to get the first lesson for the current day. 

To use your custom actions in your stories they have to be added to your projects domain.

```yml
actions:
    - schul_cloud.first-lesson.GetFirstLesson
```

## Greeting Message
In order to present the user with a short introduction of what the chatbot can do and initiate the conversation, a greeting message is rendered as soon as the chatbot is openend. 

You can find the greeting message & create your own  in the "getGreetingMessage"-function in the directory [`chat-ui/src/App.js`](chat-ui/src/App.js).
The greeting message itself is created in the same directory in the "render"-function.



## Conclusion & Reflection

This chatbot was aimed as a proof of concept project in which we tried to build a prototype support bot on the basis of openSAP data. The extracted forum datasets and frequently asked questions were largely unstructured and widely spread into several intent sets with just a few examples each.

In hindsight one of the biggest and most pressing challenges is therefore the creation of a good set of training data, which produces a model with reliable results. We faced the issue of low confidence levels in the natural language processing unit from early on. Partly due to sparse feedback in a survey to gather more examples, we were only able to increase those slightly. So further surveys and crowdsourcing with well defined intents are needed to create such training data. In addition naming conventions for intents and actions should be developed to be able maintain the only growing number of use cases.

Overall we were able to build a usable prototype with the given data and newly created ones. This prototype seems to be a good foundation for further development of a production ready support chatbot. 
