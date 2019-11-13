import os
import numpy as np

from rasa.nlu.components import Component
from rasa.nlu.classifiers import INTENT_RANKING_LENGTH
from rasa.nlu import utils

import typing
from typing import Any, Optional, Text, Dict

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class KerasNN(Component):
    """A new component"""

    language_list = None

    provides = ['intent', 'intent_ranking']

    requires = ['text_features']

    defaults = {
        # whether to use dropout
        'use_dropout': True,
        'dropout_rate': 0.5,
        # number of units in each dense layer,
        # i.e. one layer is created for each element in the list
        'n_units': [256,]
    }

    def __init__(self, component_config=None, model=None, le=None,
                 graph=None, session=None):
        from sklearn.preprocessing import LabelEncoder

        super(KerasNN, self).__init__(component_config)

        if le is not None:
            self.le = le
        else:
            self.le = LabelEncoder()
        self.model = model
        self.graph = graph
        self.session = session
    
    @classmethod
    def required_packages(cls):
        return ['sklearn', 'tensorflow']

    def _create_model(self, input_shape):
        """Create the model."""
        from tensorflow.keras import layers
        from tensorflow.keras import models

        inp = layers.Input(shape=input_shape)
        x = inp
        for units in self.component_config['n_units']:
            x = layers.Dense(units, activation='relu')(x)
        
        if self.component_config['use_dropout']:
            x = layers.Dropout(self.component_config['dropout_rate'])(x)
        
        out = layers.Dense(len(self.le.classes_), activation='softmax')(x)

        model = models.Model(inp, out)

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        return model

    def train(self, training_data, cfg, **kwargs):
        """Train this component."""
        import tensorflow as tf
        from tensorflow.keras import callbacks
        
        labels = [e.get('intent') for e in training_data.intent_examples]

        y = self.le.fit_transform(labels)
        if len(self.le.classes_) < 2:
            raise RuntimeError("The number of different intents must be at least 2.")
        
        X = np.stack(
            [
                example.get('text_features') 
                for example in training_data.intent_examples
            ]
        )

        self.graph = tf.Graph()
        with self.graph.as_default():
            self.session = tf.Session()
            with self.session.as_default():
                self.model = self._create_model(X.shape[1:])

                callback = [
                    callbacks.EarlyStopping(monitor='loss', min_delta=1e-3, patience=5,
                                            restore_best_weights=True),
                    callbacks.EarlyStopping(monitor='acc', min_delta=1e-3, patience=5,
                                            restore_best_weights=True)
                ]

                self.model.fit(X, y, batch_size=128, epochs=200, callbacks=callback)

    def process(self, message, **kwargs):
        """Process an incoming message."""
        import tensorflow
        from tensorflow.keras import backend

        if not self.model:
            # probably has not been trained yet
            intent = None
            intent_ranking = []
        else:
            X = message.get('text_features').reshape(1,-1)
            
            with self.graph.as_default(), self.session.as_default():
                intent_probs = self.model.predict(X)[0]

            if intent_probs.size > 0:
                intent_ids = np.argsort(intent_probs)[::-1]
                intents = self.le.inverse_transform(intent_ids)
                intent_probs = intent_probs[intent_ids].flatten()
                ranking = list(zip(list(intents), list(intent_probs)))[
                    :INTENT_RANKING_LENGTH
                ]

                intent = {'name': intents[0], 'confidence': float(intent_probs[0])}
                intent_ranking = [
                    {'name': intent_name, 'confidence': float(score)}
                    for intent_name, score in ranking
                ]
            else:
                intent = {'name': None, 'confidence': 0.0}
                intent_ranking = []

        message.set('intent', intent, add_to_output=True)
        message.set('intent_ranking', intent_ranking, add_to_output=True)

    def persist(self,
                file_name: Text,
                model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        model_file_name = file_name + '_model.h5'
        encoder_file_name = file_name + '_encoder.pkl'
        if self.model and self.le:
            with self.graph.as_default(), self.session.as_default():
                self.model.save(os.path.join(model_dir, model_file_name))
            utils.json_pickle(
                os.path.join(model_dir, encoder_file_name), self.le.classes_
            )
        
        return {'model': model_file_name, 'encoder': encoder_file_name}
        

    @classmethod
    def load(cls,
             meta: Dict[Text, Any],
             model_dir: Optional[Text] = None,
             model_metadata: Optional['Metadata'] = None,
             cached_component: Optional['Component'] = None,
             **kwargs: Any
             ) -> 'Component':
        """Load this component from file."""
        
        from sklearn.preprocessing import LabelEncoder
        from tensorflow.keras.models import load_model
        from tensorflow.keras import backend
        import tensorflow as tf

        model_file = os.path.join(model_dir, meta.get('model'))
        encoder_file = os.path.join(model_dir, meta.get('encoder'))

        if os.path.exists(model_file):
            graph = tf.Graph()
            with graph.as_default():
                session = tf.Session()
                with session.as_default():
                    model = load_model(model_file)
            classes = utils.json_unpickle(encoder_file)
            encoder = LabelEncoder()
            encoder.classes_ = classes
            return cls(meta, model, encoder, graph=graph, session=session)
        else:
            return cls(meta)