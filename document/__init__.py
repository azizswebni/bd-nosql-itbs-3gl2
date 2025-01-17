from flask_smorest import Blueprint

app = Blueprint("document API", __name__, description="web services document")

from . import views