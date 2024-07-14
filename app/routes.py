
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd

main = Blueprint('main', __name__)

file_path = 'plantilla_entrenamiento_completa.xlsx'

@main.route('/')
def index():
    df = pd.read_excel(file_path, sheet_name='Datos del Alumno')
    alumnos = df.to_dict(orient='records')
    return render_template('index.html', alumnos=alumnos)

@main.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    edad = request.form['edad']
    email = request.form['email']
    telefono = request.form['telefono']
    deporte = request.form['deporte']

    # Leer el archivo Excel
    df = pd.read_excel(file_path, sheet_name='Datos del Alumno')

    # Crear un nuevo DataFrame con los datos del formulario
    nuevo_alumno = pd.DataFrame({
        'Nombre': [nombre],
        'Edad': [edad],
        'Email': [email],
        'Teléfono': [telefono],
        'Deporte': [deporte]
    })

    # Añadir el nuevo alumno al DataFrame existente
    df = pd.concat([df, nuevo_alumno], ignore_index=True)

    # Guardar el DataFrame actualizado de vuelta en el archivo Excel
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='Datos del Alumno', index=False)

    return redirect(url_for('main.index'))


