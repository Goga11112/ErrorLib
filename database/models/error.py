from database.db import db

class Error(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    solution = db.Column(db.Text, nullable=False)
    images = db.relationship('ErrorImage', backref='error', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Error {self.id} {self.name}>'
