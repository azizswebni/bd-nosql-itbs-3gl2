import datetime
from run import db

class Abonnes(db.Document):
    nom = db.StringField(required=True)
    prenom = db.StringField(required=True)
    adresse = db.StringField(required=True)
    date_inscription = db.DateTimeField(default=datetime.datetime.utcnow)
    emprunts_en_cours = db.ListField(db.ReferenceField('Emprunt'))
    historique_emprunts = db.ListField(db.ReferenceField('Emprunt'))

class Documents(db.Document):
    titre = db.StringField(required=True)
    type = db.StringField(required=True, choices=["Livre", "Magazine", "DVD", "CD", "E-book"])
    auteur = db.StringField(required=True)
    date_publication = db.DateTimeField(default=datetime.datetime.utcnow)
    disponible = db.BooleanField(default=True)

class Emprunts(db.Document):
    abonne = db.ReferenceField(Abonnes, required=True)
    document = db.ReferenceField(Documents, required=True)
    date_emprunt = db.DateTimeField(default=datetime.datetime.utcnow)
    date_retour_prevue = db.DateTimeField()
    statut = db.StringField(default='en cours')