from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash
)

from extensions import db

from models.treino_modelo import (
    TreinoModelo,
    TreinoModeloExercicio
)

from models.exercicio import Exercicio


treinos_bp = Blueprint(
    'treinos',
    __name__
)


# ==================================
# LISTAR TREINOS
# ==================================
@treinos_bp.route('/treinos')
def listar_treinos():

    if session.get('tipo') != 'admin':
        return redirect('/')

    treinos = TreinoModelo.query.order_by(
        TreinoModelo.id.desc()
    ).all()

    return render_template(
        'admin/treinos/listar_treinos.html',
        treinos=treinos
    )


# ==================================
# CRIAR TREINO
# ==================================
@treinos_bp.route(
    '/criar-treino',
    methods=['GET', 'POST']
)
def criar_treino():

    if session.get('tipo') != 'admin':
        return redirect('/')

    exercicios = Exercicio.query.order_by(
        Exercicio.nome.asc()
    ).all()

    if request.method == 'POST':

        treino = TreinoModelo(
            nome=request.form['nome'],
            descricao=request.form['descricao']
        )

        db.session.add(treino)
        db.session.commit()

        exercicios_selecionados = (
            request.form.getlist(
                'exercicios'
            )
        )

        for exercicio_id in exercicios_selecionados:

            item = TreinoModeloExercicio(
                treino_id=treino.id,
                exercicio_id=int(exercicio_id)
            )

            db.session.add(item)

        db.session.commit()

        flash(
            'Treino criado com sucesso.'
        )

        return redirect('/treinos')

    return render_template(
        'admin/treinos/criar_treino.html',
        exercicios=exercicios
    )


# ==================================
# VISUALIZAR TREINO
# ==================================
@treinos_bp.route(
    '/visualizar-treino/<int:id>'
)
def visualizar_treino(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    treino = TreinoModelo.query.get_or_404(
        id
    )

    return render_template(
        'admin/treinos/visualizar_treino.html',
        treino=treino
    )


# ==================================
# EDITAR TREINO
# ==================================
@treinos_bp.route(
    '/editar-treino/<int:id>',
    methods=['GET', 'POST']
)
def editar_treino(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    treino = TreinoModelo.query.get_or_404(
        id
    )

    exercicios = Exercicio.query.order_by(
        Exercicio.nome.asc()
    ).all()

    if request.method == 'POST':

        treino.nome = request.form[
            'nome'
        ]

        treino.descricao = request.form[
            'descricao'
        ]

        TreinoModeloExercicio.query.filter_by(
            treino_id=id
        ).delete()

        exercicios_selecionados = (
            request.form.getlist(
                'exercicios'
            )
        )

        for exercicio_id in exercicios_selecionados:

            item = TreinoModeloExercicio(
                treino_id=treino.id,
                exercicio_id=int(
                    exercicio_id
                )
            )

            db.session.add(item)

        db.session.commit()

        flash(
            'Treino atualizado.'
        )

        return redirect(
            '/treinos'
        )

    selecionados = [

        item.exercicio_id

        for item in treino.itens

    ]

    return render_template(
        'admin/treinos/editar_treino.html',
        treino=treino,
        exercicios=exercicios,
        selecionados=selecionados
    )


# ==================================
# EXCLUIR TREINO
# ==================================
@treinos_bp.route(
    '/deletar-treino/<int:id>'
)
def deletar_treino(id):

    if session.get('tipo') != 'admin':
        return redirect('/')

    treino = TreinoModelo.query.get_or_404(
        id
    )

    TreinoModeloExercicio.query.filter_by(
        treino_id=id
    ).delete()

    db.session.delete(
        treino
    )

    db.session.commit()

    flash(
        'Treino removido.'
    )

    return redirect(
        '/treinos'
    )

