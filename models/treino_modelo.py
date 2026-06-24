from extensions import db


class TreinoModelo(db.Model):

    __tablename__ = 'treino_modelo'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )


class TreinoModeloExercicio(db.Model):

    __tablename__ = (
        'treino_modelo_exercicio'
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    treino_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'treino_modelo.id'
        )
    )

    exercicio_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'exercicio.id'
        )
    )

    treino = db.relationship(
        'TreinoModelo',
        backref='itens'
    )

    exercicio = db.relationship(
        'Exercicio'
    )

    