from extensions import db


class Pagamento(db.Model):

    __tablename__ = 'pagamento'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'usuario.id'
        ),
        nullable=False
    )

    valor_pago = db.Column(
        db.Float,
        nullable=False
    )

    data_pagamento = db.Column(
        db.Date,
        nullable=False
    )

    referencia_mes = db.Column(
        db.String(30)
    )

    proximo_vencimento = db.Column(
        db.Date
    )

    forma_pagamento = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(30),
        default='Pago'
    )

    observacao = db.Column(
        db.Text
    )

    aluno = db.relationship(
        'Usuario'
    )

    