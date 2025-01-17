from flask_smorest import Blueprint

app = Blueprint("emprunt API", __name__, description="web services emprunt")

from . import views