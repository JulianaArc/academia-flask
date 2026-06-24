from flask import (
    Blueprint,
    render_template,
    session,
    redirect
)

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard-admin')
def dashboard_admin():
    if session.get('tipo') != 'admin':
        return redirect('/')

    return render_template('admin/dashboard/dashboard_admin.html')

