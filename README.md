# cui
A Conversational UI experiment


## How to run:

- docker-compose up --build


Training:
 
docker-compose run rasa-nlu python -m rasa_nlu.train -d data/opensap_faq/account.md -o projects --project opensap_faq -c config.yml

Then run:

docker-compose up rasa-nlu

--> localhost:5000/parse?q=hello
