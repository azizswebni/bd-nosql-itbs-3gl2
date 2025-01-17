import datetime
from run import db
class Abonne(db.Document):
    nom = db.StringField(required=True)
    prenom = db.StringField(required=True)
    adresse = db.StringField(required=True)
    date_inscription = db.DateTimeField(default=datetime.datetime.utcnow)
    emprunts_en_cours = db.ListField(db.ReferenceField('Emprunt'))
    historique_emprunts = db.ListField(db.ReferenceField('Emprunt'))