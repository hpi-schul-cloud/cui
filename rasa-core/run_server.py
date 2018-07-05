import os
from os import environ as env
from gevent.pywsgi import WSGIServer

from server import create_app
from rasa_core import utils
from rasa_core.interpreter import RasaNLUHttpInterpreter

utils.configure_colored_logging("DEBUG")

user_input_dir = "/app/nlu/" + os.environ["RASA_NLU_PROJECT_NAME"] + "/user_input"
if not os.path.exists(user_input_dir):
    os.makedirs(user_input_dir)

nlu_interpreter = RasaNLUHttpInterpreter(
    model_name = env["RASA_NLU_MODEL_NAME"],
    token = env["RASA_NLU_SERVER_TOKEN"],
    server = env["RASA_NLU_SERVER_ADDRESS"],
    project_name = env["RASA_NLU_PROJECT_NAME"])

app = create_app(
    model_directory = env["RASA_CORE_MODEL_PATH"],
    cors_origins="*",
    loglevel = "DEBUG",
    logfile = "./logs/rasa_core.log",
    interpreter = nlu_interpreter)

http_server = WSGIServer(('0.0.0.0', 5005), app)
http_server.serve_forever()
