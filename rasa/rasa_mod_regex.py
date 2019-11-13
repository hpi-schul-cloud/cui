import os
import re
import warnings
from typing import Any, Dict, Optional, Text
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.extractors import EntityExtractor
from rasa.nlu.model import Metadata
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.utils import write_json_to_file
import rasa.utils.io

class RegexEntityExtractor(EntityExtractor):
    # This extractor maybe kind of extreme as it takes user's message
    # and return regex match.
    # Confidence will be 1.0 just like Duckling

    provides = ["entities"]

    def __init__(
        self,
        component_config: Optional[Dict[Text, Text]] = None,
        regex_features: Optional[Dict[Text, Any]] = None
    ) -> None:
        super(RegexEntityExtractor, self).__init__(component_config)

        self.regex_feature = regex_features if regex_features else {}

    def train(
        self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:

        self.regex_feature = training_data.regex_features

    @classmethod
    def load(
            cls,
            meta: Dict[Text, Any],
            model_dir: Optional[Text] = None,
            model_metadata: Optional[Metadata] = None,
            cached_component: Optional["RegexEntityExtractor"] = None,
            **kwargs: Any
    ) -> "RegexEntityExtractor":

        file_name = meta.get("file")

        if not file_name:
            regex_features = None
            return cls(meta, regex_features)

        # w/o string cast, mypy will tell me
        # expected "Union[str, _PathLike[str]]"
        regex_pattern_file = os.path.join(str(model_dir), file_name)
        if os.path.isfile(regex_pattern_file):
            regex_features = rasa.utils.io.read_json_file(regex_pattern_file)
        else:
            regex_features = None
            warnings.warn(
                "Failed to load regex pattern file from '{}'".format(regex_pattern_file)
            )
        return cls(meta, regex_features)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""
        if self.regex_feature:
            file_name = file_name + ".json"
            regex_feature_file = os.path.join(model_dir, file_name)
            write_json_to_file(
                regex_feature_file,
                self.regex_feature, separators=(",", ": "))
            return {"file": file_name}
        else:
            return {"file": None}

    def match_regex(self, message):
        extracted = []
        for d in self.regex_feature:
            match = re.search(pattern=d['pattern'], string=message)
            if match:

                entity = {
                    "start": match.pos,
                    "end": match.endpos,
                    "value": match.group(),
                    "confidence": 1.0,
                    "entity": d['name'],
                }
                extracted.append(entity)

        extracted = self.add_extractor_name(extracted)
        return extracted

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""
        extracted = self.match_regex(message.text)
        message.set(
            "entities", message.get("entities", []) + extracted, add_to_output=True
        )