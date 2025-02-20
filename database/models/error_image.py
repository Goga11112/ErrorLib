from db import db

class ErrorImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    error_id = db.Column(db.Integer, db.ForeignKey('error.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint("type IN ('error', 'solution')", name='type_check'),
    )
