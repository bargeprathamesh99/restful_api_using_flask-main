from flask import Flask

app = Flask(__name__)

from controller import user_controller
from model import user_model