from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from extensions import db

from models.plano import Plano
from models.usuario import Usuario

planos_bp = Blueprint(
    'planos',
    __name__
)

@planos_bp.route('/planos')
def listar_planos():

    if session.get('tipo') != 'admin':
        return redirect('/')

    planos = Plano.query.order_by(
        Plano.id.asc()
    ).all()

    return render_template(
        'admin/planos/listar_planos.html',
        planos=planos
    )


@planos_bp.route(
    '/cadastrar-plano',
    methods=['GET', 'POST']
)
def cadastrar_plano():

    if session.get('tipo') != 'admin':
        return redirect('/')

    if request.method == 'POST':

        novo_plano = Plano(
            nome=request.form['nome'],
            categoria=request.form['categoria'],
            horario=request.form['horario'],
            valor=float(request.form['valor']),
            beneficios=request.form['beneficios'],
            status=request.form['status']
        )

        db.session.add(
            novo_plano
        )

        db.session.commit()

        flash(
            'Plano cadastrado com sucesso.'
        )

        return redirect('/planos')

    return render_template(
        'admin/planos/cadastrar_plano.html'
    )


@planos_bp.route(
    '/editar-plano/<int:id>',
    methods=['GET', 'POST']
)
def editar_plano(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    plano = Plano.query.get_or_404(
        id
    )

    if request.method == 'POST':

        plano.nome = request.form['nome']

        plano.categoria = request.form['categoria']

        plano.horario = request.form['horario']

        plano.valor = float(
            request.form['valor']
        )

        plano.beneficios = request.form[
            'beneficios'
        ]

        plano.status = request.form[
            'status'
        ]

        db.session.commit()

        flash(
            'Plano atualizado.'
        )

        return redirect('/planos')

    return render_template(
        'admin/planos/editar_plano.html',
        plano=plano
    )


@planos_bp.route(
    '/deletar-plano/<int:id>'
)
def deletar_plano(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    plano = Plano.query.get_or_404(
        id
    )

    total_alunos = Usuario.query.filter_by(
        plano_id=plano.id
    ).count()

    if total_alunos > 0:

        flash(
            f'Não é possível excluir este plano. Existem {total_alunos} alunos vinculados.'
        )

        return redirect('/planos')

    db.session.delete(plano)

    db.session.commit()

    flash(
        'Plano removido.'
    )

    return redirect('/planos')

