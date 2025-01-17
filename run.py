from flask import Flask, jsonify,render_template,Response,request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_pymongo import PyMongo
import os



from flask_smorest import Api
from abonnee import app as abonnee_app
from emprunt import app as emprunt_app
from document import app as document_app
from flask_mongoengine import MongoEngine

app = Flask(__name__,template_folder='static')
app.config["API_TITLE"] = "MEDIATHEQUE"
app.config["API_VERSION"] = "v1.0.5"
app.config["OPENAPI_VERSION"] = "3.0.1"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mediatheque"
db = MongoEngine(app)

CORS(app)

api = Api(app)
api.register_blueprint(abonnee_app,url_prefix="/abonnee")
api.register_blueprint(emprunt_app,url_prefix="/emprunt")
api.register_blueprint(document_app,url_prefix="/document")

@app.route('/developer')
def get_doc():
    swaggerURL = "./static/swaggerrcpro.yaml"
    with open(os.path.realpath("static/index.html"), 'r') as file:
        data = file.read().replace('\n', '').replace("swaggerUrl",swaggerURL)
    return data

SWAGGER_URL = "/mediatheque/Docs"
API_URL = "/static/swagger.yaml"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "MEDIATHEQUE"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

DOCS_URL = "/static/index.html"

if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()