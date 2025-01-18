import datetime
from flask import jsonify, render_template, request
from bson import ObjectId
from . import app
from flask.views import MethodView

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()

def make_document_available(document_id):
    from abonnee.models import Abonnes, Documents, Emprunts
    document = Documents.objects(id=document_id).first()
    if document:
        document.update(set__disponible=True)
        print(f"Document {document_id} is now available.")

@app.route('/insert_emprunt', methods=['POST'])
def insert_emprunt():
    data = request.json

    abonne = Abonnes.objects(id=data["abonne_id"]).first()
    document = Documents.objects(id=data["document_id"]).first()

    if not abonne or not document:
        return jsonify({"message": "Abonné ou document non trouvé"}), 404

    nouvel_emprunt = Emprunts(
        abonne=abonne,
        document=document,
        date_retour_prevue=data["date_retour_prevue"]
    )

    nouvel_emprunt.save()
    document.update(set__disponible=False)

    date_retour_prevue = datetime.strptime(data["date_retour_prevue"], "%Y-%m-%d %H:%M:%S")
    scheduler.add_job(
        make_document_available,
        trigger="date",
        run_date=date_retour_prevue,
        args=[str(document.id)],
        id=f"make_document_available_{document.id}",
        replace_existing=True
    )

    return jsonify({"message": "Emprunt ajouté avec succès", "id": str(nouvel_emprunt.id)}), 201


@app.route('/get_emprunts', methods=['GET'])
def get_emprunts():
    from abonnee.models import Abonnes, Documents, Emprunts
    emprunts = Emprunts.objects()
    abonnes = Abonnes.objects()
    documents = Documents.objects()

    documents_list = []
    for doc in documents:
        if doc.disponible:
            documents_list.append({
            "_id": str(doc.id),
            "titre": doc.titre,
            "type": doc.type,
            "auteur": doc.auteur,
            "date_publication": doc.date_publication.isoformat(),
            "disponible": doc.disponible
            })

    return render_template('emp.html', emprunts=emprunts,abonnes=abonnes,documents=documents_list)

@app.route('/get_emprunt/<id_emprunt>', methods=['GET'])
def get_emprunt(id_emprunt):
    from abonnee.models import Abonnes, Documents, Emprunts
    emprunt = Emprunts.objects(id=id_emprunt).first()

    if not emprunt:
        return jsonify({"message": "Emprunt non trouvé"}), 404

    emprunt_data = {
        "_id": str(emprunt.id),
        "abonne_id": str(emprunt.abonne.id),
        "document_id": str(emprunt.document.id),
        "date_emprunt": emprunt.date_emprunt.isoformat(),
        "date_retour_prevue": emprunt.date_retour_prevue.isoformat(),
        "statut": emprunt.statut
    }

    return jsonify(emprunt_data), 200

@app.route('/delete_emprunt/<id_emprunt>', methods=['DELETE'])
def delete_emprunt(id_emprunt):
    from abonnee.models import Abonnes, Documents, Emprunts
    emprunt = Emprunts.objects(id=id_emprunt).first()
    if not emprunt:
        return jsonify({"message": "Emprunt non trouvé"}), 404

    emprunt.delete()

    return jsonify({"message": "Emprunt supprimé avec succès"}), 200

@app.route('/get_emprunts_abonne/<id_abonne>', methods=['GET'])
def get_emprunts_abonne(id_abonne):
    from abonnee.models import Abonnes, Documents, Emprunts
    abonne = Abonnes.objects(id=id_abonne).first()
    if not abonne:
        return jsonify({"message": "Abonné non trouvé"}), 404

    emprunts = Emprunts.objects(abonne=abonne)

    emprunts_list = []
    for emprunt in emprunts:
        emprunts_list.append({
            "_id": str(emprunt.id),
            "document_id": str(emprunt.document.id),
            "date_emprunt": emprunt.date_emprunt.isoformat(),
            "date_retour_prevue": emprunt.date_retour_prevue.isoformat(),
            "statut": emprunt.statut
        })

    return jsonify(emprunts_list)
