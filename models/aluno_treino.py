from extensions import db


class AlunoTreino(db.Model):

    __tablename__ = 'aluno_treino'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'usuario.id'
        )
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    origem = db.Column(
        db.String(50),
        default='personalizado'
    )

    aluno = db.relationship(
        'Usuario'
    )


class AlunoTreinoExercicio(db.Model):

    __tablename__ = (
        'aluno_treino_exercicio'
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    treino_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'aluno_treino.id'
        )
    )

    exercicio_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'exercicio.id'
        )
    )

    peso = db.Column(
        db.Float
    )

    series = db.Column(
        db.Integer
    )

    repeticoes = db.Column(
        db.Integer
    )

    treino = db.relationship(
        'AlunoTreino',
        backref='exercicios'
    )

    exercicio = db.relationship(
        'Exercicio'
    )

    