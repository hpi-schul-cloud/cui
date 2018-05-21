from os import environ as env
from rasa_core.server import RasaCoreServer
from rasa_core.interpreter import RasaNLUHttpInterpreter

nlu_interpreter = RasaNLUHttpInterpreter(
    model_name = env["RASA_NLU_MODEL_NAME"],
    token = env["RASA_NLU_SERVER_TOKEN"],
    server = env["RASA_NLU_SERVER_ADDRESS"],
    project_name = env["RASA_NLU_PROJECT_NAME"])

rasa = RasaCoreServer(env["RASA_CORE_MODEL_PATH"], interpreter = nlu_interpreter)
rasa.app.run("0.0.0.0", 5005)