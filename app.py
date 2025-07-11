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
        numh = row_dict.get("numhorario")
        if numh == 14:
            row_dict["numhorario"] = 8
        elif 8 <= numh <= 13:
            row_dict["numhorario"] = numh + 1

        limpio = {k: row_dict[k] for k in columnas_permitidas if k in row_dict}
        data.append(limpio)

    data = sorted(data, key=lambda x: x.get("numhorario", 0))
    #for fila in data:
     #   fila.pop("numhorario", None)

    return render_template(
        "agenda.html",
        agenda=data,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        offset=offset  # útil si luego querés mostrar navegación dinámica
    )

if __name__ == "__main__":
    app.run(debug=True)
