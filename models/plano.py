from extensions import db


class Plano(db.Model):

    __tablename__ = 'plano'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    categoria = db.Column(
        db.String(50),
        nullable=False
    )

    horario = db.Column(
        db.String(100),
        nullable=False
    )

    valor = db.Column(
        db.Float
    )

    beneficios = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(30),
        default='Disponível'
    )

    arquivado = db.Column(
        db.Boolean,
        default=False
    )

    usuarios = db.relationship(
        'Usuario',
        backref='plano',
        lazy=True
    )

    