from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from dbconn import get_connection

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT usuario FROM JCORNEJOR.USUARIOHORIRO WHERE usuario = ? AND clave = ?",
            (usuario, clave)
        )
        resultado = cursor.fetchone()

        if resultado:
            session['usuario'] = usuario
            return redirect(url_for('mostrar_agenda'))  # Asegúrate que esta vista exista
        else:
            flash('Usuario o clave incorrectos', 'danger')

    return render_template('login.html')
