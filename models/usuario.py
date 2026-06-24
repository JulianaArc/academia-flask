from extensions import db


class Usuario(db.Model):

    __tablename__ = 'usuario'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    cpf = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    telefone = db.Column(
        db.String(20)
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )

    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        default=False
    )

    plano_id = db.Column(
        db.Integer,
        db.ForeignKey('plano.id')
    )

    data_matricula = db.Column(
        db.Date,
        nullable=True
    )

    proximo_vencimento = db.Column(
        db.Date,
        nullable=True
    )

    status_pagamento = db.Column(
        db.String(30),
        default='Pendente'
    )
    