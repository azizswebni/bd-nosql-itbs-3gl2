
import datetime
from flask import jsonify, render_template, request

from abonnee.models import Abonne

from . import app
from flask.views import MethodView
from bson import ObjectId
from run import db

@app.route('/insert_abonnee', methods=['POST'])
def ajouter_abonne():
    data = request.json

    # Vérifier que les champs obligatoires sont fournis
    if not all(k in data for k in ["nom", "prenom", "adresse"]):
        return jsonify({"message": "Les champs 'nom', 'prenom' et 'adresse' sont obligatoires"}), 400

    nouvel_abonne = Abonne(
        nom=data["nom"],
        prenom=data["prenom"],
        adresse=data["adresse"],
        date_inscription=datetime.datetime.utcnow()
    )

    nouvel_abonne.save()

    return jsonify({"message": "Abonné ajouté avec succès", "id": str(nouvel_abonne.id)}), 201

@app.route('/get_abonnes', methods=['GET'])
def get_abonnes():
    abonnés = Abonne.objects()

    abonnés_list = []
    for abonne in abonnés:
        abonnés_list.append({
            "_id": str(abonne.id),
            "nom": abonne.nom,
            "prenom": abonne.prenom,
            "adresse": abonne.adresse,
            "date_inscription": abonne.date_inscription.isoformat()
        })

    return jsonify(abonnés_list),200

@app.route('/update_abonnes/<id_abonne>', methods=['PUT'])
def modifier_abonne(id_abonne):
    data = request.json

    abonne = Abonne.objects(id=id_abonne).first()

    if not abonne:
        return jsonify({"message": "Abonné non trouvé"}), 404

    abonne.update(
        set__nom=data["nom"],
        set__prenom=data["prenom"],
        set__adresse=data["adresse"]
    )

    return jsonify({"message": "Abonné modifié avec succès"}), 200

@app.route('/delete_abonnee/<id_abonne>', methods=['DELETE'])
def supprimer_abonne(id_abonne):
    abonne = Abonne.objects(id=id_abonne).first()
    if not abonne:
        return jsonify({"message": "Abonné non trouvé"}), 404

    abonne.delete()

    return jsonify({"message": "Abonné supprimé avec succès"}), 200