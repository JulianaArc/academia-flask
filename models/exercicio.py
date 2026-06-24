from extensions import db


class Exercicio(db.Model):

    __tablename__ = 'exercicio'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    grupo_muscular = db.Column(
        db.String(100)
    )

    descricao = db.Column(
        db.Text
    )

    peso_padrao = db.Column(
        db.Float
    )

    series_padrao = db.Column(
        db.Integer
    )

    repeticoes_padrao = db.Column(
        db.Integer
    )

    