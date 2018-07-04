#!/bin/sh

cd /app
python -m rasa_nlu.train -d data/opensap_faq -o projects --project opensap_faq -c config.yml
