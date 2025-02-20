from database.db import db

class ErrorTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    responsible = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<ErrorTopic {self.id} {self.topic}>'
