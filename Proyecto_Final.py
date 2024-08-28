from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql

app = Flask(__name__)

conn = sql.connect('farmacias.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Farmacias (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    ciudad TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Empleados (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    apellido TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    num_empleado TEXT,
                    clave_sucursal TEXT,
                    puesto TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Laboratorios (
                    id INTEGER PRIMARY KEY,
                    laboratorio TEXT,
                    direccion TEXT,
                    telefono TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Medicamentos (
                    id INTEGER PRIMARY KEY,
                    cantidad TEXT,
                    nombre_comercial TEXT,
                    presentacion TEXT,
                    accion_terapeutica TEXT,
                    labortorio TEXT,
                    precio TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
                    id INTEGER PRIMARY KEY,
                    id_stock TEXT,
                    Medicamento TEXT,
                    presentacion TEXT
                )''')

conn.commit()
conn.close()

@app.route('/')
def datos():
    return render_template("datos.html")

@app.route('/guardar', methods=["POST"])
def guardar():
    if request.method == "POST":
        nombreF = request.form['nombre_farmacia']
        direccion = request.form['direccion_farmacia']
        telefono = request.form['telefono_farmacia']
        ciudad = request.form['ciudad_farmacia']

        conn = sql.connect('farmacias.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Farmacias (nombre, direccion, telefono, ciudad) VALUES (?, ?, ?, ?)",
                       (nombreF, direccion, telefono, ciudad))
        conn.commit()

        personal = int(request.form['numero_empleados'])
        for i in range(personal):
            nombreP = request.form['nombre_empleado{}'.format(i)]
            apellido = request.form['apellido_empleado{}'.format(i)]
            direccion2 = request.form['direccion_empleado{}'.format(i)]
            telefono2 = request.form['telefono_empleado{}'.format(i)]
            nempleado = request.form['num_empleado{}'.format(i)]
            clave = request.form['clave_sucursal{}'.format(i)]
            puesto = request.form['puesto{}'.format(i)]
           

            cursor.execute("INSERT INTO Empleados (nombre, apellido, direccion, telefono, num_empleado, clave_sucursal, puesto) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (nombreP, apellido, direccion2, telefono2, nempleado, clave, puesto))
            conn.commit()


        conn.close()
        return redirect(url_for('guardado'))
    
    
@app.route('/guardado')
def guardado():
    return render_template("guardado.html")

@app.route('/guardar2')
def segunda():
    return render_template("laboratorio.html")

@app.route('/tercera')
def tercera():
    return render_template("guardado2.html")

@app.route('/guardar1', methods=["POST"])
def laboratorio():
    if request.method == "POST":
        laboratorio = request.form['laboratorio']
        direccionL = request.form['direccionL']
        telefono3 = request.form['telefono3']

        conn = sql.connect('farmacias.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Laboratorios (laboratorio, direccion, telefono) VALUES (?, ?, ?)",
                       (laboratorio, direccionL, telefono3))
        conn.commit()

        idS =  request.form['idstock']
        nS =  request.form['nS']
        pS =  request.form['pS']
        conn = sql.connect('farmacias.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Stock (id_stock, Medicamento, presentacion) VALUES (?, ?, ?)",
                       (idS,nS,pS))
        conn.commit()

        medicamentos = int(request.form['medicamentos'])
        for i in range(medicamentos):
            cantidad = request.form['cantidad{}'.format(i)]
            nombre_comercial = request.form['nombre_medicamento_{}'.format(i)]
            presentacion = request.form['presentacion_medicamento_{}'.format(i)]
            accion_terapeutica = request.form['accion_terapeutica_medicamento_{}'.format(i)]
            laboratorio = request.form['laboratorio{}'.format(i)]
            precio = request.form['precio{}'.format(i)]

            cursor.execute("INSERT INTO Medicamentos (cantidad, nombre_comercial, presentacion, accion_terapeutica, labortorio,  precio) VALUES (?, ?, ?, ?, ?, ?)",
                           (cantidad, nombre_comercial, presentacion, accion_terapeutica, laboratorio, precio))
            conn.commit()

        conn.close()

        return redirect(url_for('tercera'))


@app.route('/buscar_medicamento', methods=['GET', 'POST'])
def buscar_medicamento():
    if request.method == 'POST':
        termino_busqueda = request.form.get('termino_busqueda', '')

        conn = sql.connect('farmacias.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Medicamentos WHERE cantidad LIKE ? OR nombre_comercial LIKE ? OR presentacion LIKE ? OR labortorio LIKE ? OR precio LIKE ?", 
                        ('%'+termino_busqueda+'%','%'+termino_busqueda+'%', '%'+termino_busqueda+'%', '%'+termino_busqueda+'%', '%'+termino_busqueda+'%'))
        resultados = cursor.fetchall()
        conn.close()

        resultados_dict = []
        for row in resultados:
            resultado_dict = {
                'id': row[0],
                'cantidad': row[1],
                'nombre_comercial': row[2],
                'presentacion': row[3],
                'accion_terapeutica': row[4],
                'labortorio': row[5],
                'precio': row[6]
            }
            resultados_dict.append(resultado_dict)

        return render_template("mostrar_resultados.html", resultados=resultados_dict)
    else:
        return render_template("buscar_medicamento.html")

if __name__ == '__main__':
    app.run(debug=True)
