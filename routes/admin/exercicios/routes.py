from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from extensions import db

from models.exercicio import Exercicio

exercicios_bp = Blueprint(
    'exercicios',
    __name__
)

@exercicios_bp.route('/exercicios')
def listar_exercicios():

    if session.get('tipo') != 'admin':
        return redirect('/')

    exercicios = Exercicio.query.order_by(
        Exercicio.id.asc()
    ).all()

    return render_template(
        'admin/exercicios/listar_exercicios.html',
        exercicios=exercicios
    )


@exercicios_bp.route(
    '/cadastrar-exercicio',
    methods=['GET', 'POST']
)
def cadastrar_exercicio():

    if session.get('tipo') != 'admin':
        return redirect('/')

    if request.method == 'POST':

        novo_exercicio = Exercicio(
            nome=request.form['nome'],
            grupo_muscular=request.form['grupo_muscular'],
            descricao=request.form['descricao'],
            peso_padrao=float(
                request.form['peso_padrao']
            ),
            series_padrao=int(
                request.form['series_padrao']
            ),
            repeticoes_padrao=int(
                request.form['repeticoes_padrao']
            )
        )

        db.session.add(
            novo_exercicio
        )

        db.session.commit()

        flash(
            'Exercício cadastrado.'
        )

        return redirect(
            '/exercicios'
        )

    return render_template(
        'admin/exercicios/cadastrar_exercicio.html'
    )



@exercicios_bp.route(
    '/editar-exercicio/<int:id>',
    methods=['GET', 'POST']
)
def editar_exercicio(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    exercicio = Exercicio.query.get_or_404(
        id
    )

    if request.method == 'POST':

        exercicio.nome = request.form['nome']

        exercicio.grupo_muscular = request.form[
            'grupo_muscular'
        ]

        exercicio.descricao = request.form[
            'descricao'
        ]

        exercicio.peso_padrao = float(
            request.form['peso_padrao']
        )

        exercicio.series_padrao = int(
            request.form['series_padrao']
        )

        exercicio.repeticoes_padrao = int(
            request.form['repeticoes_padrao']
        )

        db.session.commit()

        flash(
            'Exercício atualizado.'
        )

        return redirect(
            '/exercicios'
        )

    return render_template(
        'admin/exercicios/editar_exercicio.html',
        exercicio=exercicio
    )



@exercicios_bp.route(
    '/deletar-exercicio/<int:id>'
)
def deletar_exercicio(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    exercicio = Exercicio.query.get_or_404(
        id
    )

    db.session.delete(
        exercicio
    )

    db.session.commit()

    flash(
        'Exercício removido.'
    )

    return redirect(
        '/exercicios'
    )

