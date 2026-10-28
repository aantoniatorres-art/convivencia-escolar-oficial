from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_convivencia_escolar'

niveles_basica = [f"{i}° Básico" for i in range(1, 9)]
niveles_media = [f"{i}° Medio" for i in range(1, 5)]
secciones = ["A", "B"]

nombres_propios = ["Sofía", "Matías", "Valentina", "Lucas", "Isidora", "Benjamín", "Martina", "Agustín", "Catalina", "Vicente"]
apellidos = ["Pérez", "Gómez", "Soto", "Muñoz", "Rojas", "Silva", "Morales", "Contreras", "González", "Rodríguez"]

# Profesores con información extendida y profesional
PROFESORES = {
    1: {
        "id": 1, "nombre": "Prof. Ana Torres", "correo": "ana.torres@colegio.cl", "curso": "1° Básico A", 
        "telefono": "+56 9 8765 4321", "departamento": "Ciclo Inicial / Básica", "asignatura": "Educación General Básica", 
        "anos_servicio": 7, "oficina": "Oficina Básica 101", "horario_atencion": "Lunes 09:00 - 10:30",
        "alertas_enviadas": 4, "asistencias_registradas": 42, "estado": "Activo"
    },
    2: {
        "id": 2, "nombre": "Prof. Carlos Ruiz", "correo": "carlos.ruiz@colegio.cl", "curso": "1° Básico B", 
        "telefono": "+56 9 7654 3210", "departamento": "Ciclo Inicial / Básica", "asignatura": "Matemáticas y Ciencias", 
        "anos_servicio": 4, "oficina": "Oficina Básica 103", "horario_atencion": "Martes 11:00 - 12:30",
        "alertas_enviadas": 2, "asistencias_registradas": 38, "estado": "Activo"
    },
    3: {
        "id": 3, "nombre": "Prof. Marcela Soto", "correo": "marcela.soto@colegio.cl", "curso": "1° Medio A", 
        "telefono": "+56 9 6543 2109", "departamento": "Educación Media", "asignatura": "Lenguaje y Comunicación", 
        "anos_servicio": 12, "oficina": "Pabellón Media 204", "horario_atencion": "Jueves 10:00 - 11:30",
        "alertas_enviadas": 7, "asistencias_registradas": 45, "estado": "Activo"
    },
    4: {
        "id": 4, "nombre": "Prof. Juan Pérez", "correo": "juan.perez@colegio.cl", "curso": "2° Medio A", 
        "telefono": "+56 9 5432 1098", "departamento": "Educación Media", "asignatura": "Historia y Geografía", 
        "anos_servicio": 9, "oficina": "Pabellón Media 208", "horario_atencion": "Viernes 12:00 - 13:30",
        "alertas_enviadas": 1, "asistencias_registradas": 40, "estado": "Observación"
    }
}

CURSOS = {}
est_id = 1
prof_id_counter = 5

for nivel in niveles_basica + niveles_media:
    for sec in secciones:
        nombre_curso = f"{nivel} {sec}"
        
        curso_registrado = False
        for p in PROFESORES.values():
            if p['curso'] == nombre_curso:
                curso_registrado = True
                break
                
        if not curso_registrado:
            PROFESORES[prof_id_counter] = {
                "id": prof_id_counter,
                "nombre": f"Prof. Encargado {nombre_curso}",
                "correo": f"docente.{nombre_curso.lower().replace(' ', '').replace('°', '')}@colegio.cl",
                "curso": nombre_curso,
                "telefono": f"+56 9 {str(40000000 + prof_id_counter)[-8:]}",
                "departamento": "Educación Básica" if "Básico" in nombre_curso else "Educación Media",
                "asignatura": "Jefatura de Curso / Asignaturas Varias",
                "anos_servicio": (prof_id_counter % 8) + 1,
                "oficina": f"Sala Docentes #{prof_id_counter}",
                "horario_atencion": "Martes 15:00 - 16:30",
                "alertas_enviadas": prof_id_counter % 3,
                "asistencias_registradas": 30 + (prof_id_counter % 15),
                "estado": "Activo"
            }
            prof_id_counter += 1
        
        CURSOS[nombre_curso] = []
        for j in range(10):
            nombre_aleatorio = f"{nombres_propios[(est_id * 3) % len(nombres_propios)]} {apellidos[(est_id * 7) % len(apellidos)]} ({sec})"
            correo_base = nombre_aleatorio.lower().replace(' ', '.').replace('(', '').replace(')', '').replace('á', 'a').replace('í', 'i')
            
            CURSOS[nombre_curso].append({
                "id": est_id,
                "nombre": nombre_aleatorio,
                "correo": f"{correo_base}.{est_id}@colegio.cl",
                "telefono": f"+56 9 {str(40000000 + est_id)[-8:]}",
                "atrasos": est_id % 5,
                "convivencia": est_id % 3,
                "enfermeria": est_id % 4,
                "suspensiones": 1 if est_id % 9 == 0 else 0,
                "estado": "Al día" if (est_id % 4 != 0) else ("Observación" if est_id % 2 == 0 else "Crítico")
            })
            est_id += 1

CODIGOS_ACCESO = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        profesor_encontrado = None
        for datos in PROFESORES.values():
            if datos['correo'] == correo:
                profesor_encontrado = datos
                break
        
        if profesor_encontrado or correo == "admin@colegio.cl":
            codigo = str(random.randint(1000, 9999))
            CODIGOS_ACCESO[correo] = codigo
            
            print("\n" + "="*50)
            print(f"[CORREO SALIENTE] Destino: {correo}")
            print(f"CÓDIGO DE ACCESO SEGURO: {codigo}")
            print("="*50 + "\n")
            
            return render_template('verificar.html', correo=correo)
        else:
            return render_template('login.html', error="Correo no registrado en el sistema.")
            
    return render_template('login.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    correo = request.form.get('correo')
    codigo_ingresado = request.form.get('codigo')
    
    if correo in CODIGOS_ACCESO and CODIGOS_ACCESO[correo] == codigo_ingresado:
        session['usuario'] = correo
        return redirect(url_for('index'))
    else:
        return render_template('verificar.html', correo=correo, error="Código incorrecto o expirado.")

@app.route('/panel')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    cursos_basica = [c for c in CURSOS.keys() if "Básico" in c]
    cursos_media = [c for c in CURSOS.keys() if "Medio" in c]
    return render_template('index.html', cursos_basica=cursos_basica, cursos_media=cursos_media)

@app.route('/curso/<nombre_curso>')
def ver_curso(nombre_curso):
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    estudiantes = CURSOS.get(nombre_curso, [])
    profesor = next((p for p in PROFESORES.values() if p['curso'] == nombre_curso), {"nombre": "No asignado", "correo": "N/A"})
    return render_template('curso.html', curso=nombre_curso, estudiantes=estudiantes, profesor=profesor)

@app.route('/curso/<nombre_curso>/estudiante/<int:estudiante_id>')
def ver_estudiante(nombre_curso, estudiante_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    estudiantes = CURSOS.get(nombre_curso, [])
    estudiante = next((est for est in estudiantes if est['id'] == estudiante_id), None)
    
    if not estudiante:
        return "Estudiante no encontrado", 404
        
    return render_template('estudiante.html', curso=nombre_curso, estudiante=estudiante)

@app.route('/profesores', methods=['GET', 'POST'])
def profesores():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    global prof_id_counter
    if request.method == 'POST':
        nombre_prof = request.form.get('nombre')
        correo_prof = request.form.get('correo')
        curso_asociado = request.form.get('curso')
        telefono_prof = request.form.get('telefono', '+56 9 9999 9999')
        departamento_prof = request.form.get('departamento', 'General')
        asignatura_prof = request.form.get('asignatura', 'Asignatura General')
        oficina_prof = request.form.get('oficina', 'Sala Docentes')
        
        if curso_asociado and nombre_prof and correo_prof:
            PROFESORES[prof_id_counter] = {
                "id": prof_id_counter,
                "nombre": nombre_prof,
                "correo": correo_prof,
                "curso": curso_asociado,
                "telefono": telefono_prof,
                "departamento": departamento_prof,
                "asignatura": asignatura_prof,
                "anos_servicio": 1,
                "oficina": oficina_prof,
                "horario_atencion": "A coordinar",
                "alertas_enviadas": 0,
                "asistencias_registradas": 0,
                "estado": "Activo"
            }
            prof_id_counter += 1
        return redirect(url_for('profesores'))
        
    return render_template('profesores.html', profesores=PROFESORES.values(), cursos=CURSOS.keys())

@app.route('/profesor/<int:profesor_id>')
def ver_profesor(profesor_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    profesor = PROFESORES.get(profesor_id)
    if not profesor:
        return "Profesor no encontrado", 404
        
    return render_template('profesor_detalle.html', profesor=profesor)

@app.route('/registrar_falta', methods=['POST'])
def registrar_falta():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    curso = request.form.get('curso')
    estudiante_id = int(request.form.get('estudiante_id'))
    tipo_registro = request.form.get('tipo_registro')
    detalle_falta = request.form.get('detalle_falta')
    
    estudiante_encontrado = None
    for est in CURSOS.get(curso, []):
        if est['id'] == estudiante_id:
            estudiante_encontrado = est
            if tipo_registro == 'atraso':
                est['atrasos'] += 1
            elif tipo_registro == 'convivencia':
                est['convivencia'] += 1
            elif tipo_registro == 'enfermeria':
                est['enfermeria'] += 1
            elif tipo_registro == 'suspension':
                est['suspensiones'] += 1
            
            est['estado'] = "Observación"
            break
            
    profesor_asignatura = next((p for p in PROFESORES.values() if p['curso'] == curso), {"correo": "docente@colegio.cl"})
    
    print("\n" + "="*50)
    print(f"[NOTIFICACIÓN ENVIADA AL DOCENTE: {profesor_asignatura['correo']}]")
    print(f"Curso: {curso} | Alumno: {estudiante_encontrado['nombre'] if estudiante_encontrado else 'N/A'}")
    print(f"Categoría: {tipo_registro.upper()} | Detalle: '{detalle_falta}'")
    print("="*50 + "\n")
    
    return redirect(url_for('ver_curso', nombre_curso=curso))

@app.route('/reportes')
def reportes():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    total_cursos = len(CURSOS)
    total_estudiantes = sum(len(est) for est in CURSOS.values())
    return render_template('reportes.html', total_cursos=total_cursos, total_estudiantes=total_estudiantes)

@app.route('/configuracion')
def configuracion():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('configuracion.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 