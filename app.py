from flask import Flask, render_template, session, redirect, url_for, request
from dbconn import get_connection
from controllers.login_controller import login
from datetime import timedelta, date, datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_super_secreta'
app.permanent_session_lifetime = timedelta(days=3)
app.register_blueprint(login)

def obtener_rango_semana(offset=0):
    hoy = date.today()
    lunes = hoy - timedelta(days=hoy.weekday()) + timedelta(weeks=offset)
    sabado = lunes + timedelta(days=5)
    return lunes, sabado  # Objetos tipo date

@app.route("/")
def mostrar_agenda():
    if 'usuario' not in session:
        return redirect(url_for('login.login_view'))

    # Determinar el offset de semanas
    if request.args.get("anterior") == "1":
        offset = -1
    elif request.args.get("siguiente") == "1":
        offset = 1
    else:
        offset = 0

    fecha_inicio, fecha_fin = obtener_rango_semana(offset=offset)

    # Ejecutar SP
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "EXEC dbo.sp_reservas_consulta ?, ?",
        fecha_inicio.strftime("%Y%m%d"),
        fecha_fin.strftime("%Y%m%d")
    )

    while cursor.description is None:
        if not cursor.nextset():
            return "No se encontraron datos en el procedimiento almacenado."

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    data = []
    columnas_permitidas = ["horario", "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "numhorario"]

    for row in rows:
        row_dict = dict(zip(columns, row))
        limpio = {k: row_dict[k] for k in columnas_permitidas if k in row_dict}
        data.append(limpio)

    # Diccionario de orden cronológico de los horarios
    orden_horario = {
        17: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7,
        7: 8, 14: 9, 15: 10, 8: 11, 9: 12, 10: 13, 11: 14, 12: 15, 13:16
    }

    # Ordenar la data usando el diccionario
    data = sorted(data, key=lambda x: orden_horario.get(x.get("numhorario", 1000)))

    return render_template(
        "agenda.html",
        agenda=data,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        offset=offset  # útil si luego querés mostrar navegación dinámica
    )

if __name__ == "__main__":
    app.run(debug=True)


