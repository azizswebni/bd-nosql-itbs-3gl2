from flask_smorest import Blueprint

app = Blueprint("abonnee API", __name__, description="web services abonnee")

from . import views