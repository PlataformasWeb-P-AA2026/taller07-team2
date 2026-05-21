# poblar_base.py
import csv
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from clases import engine, Departamento, Instructor, Curso, Estudiante, Inscripcion, Tarea, Entrega
 
# Configurar la sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("Iniciando la carga de datos desde archivos CSV...")

    # 1. Cargar Departamento
    with open('01_departamento.csv', mode='r', encoding='utf-8') as f:
        # Se usa delimiter=None o se detecta si están separados por tabulación o comas
        # Si tus archivos usan espacios o tabulaciones, puedes configurar delimiter='\t'
        lector = csv.DictReader(f)
        for fila in lector:
            session.add(Departamento(
                id=int(fila['id']), 
                nombre=fila['nombre'].strip()
            ))
    print("[OK] 01_departamento.csv procesado.")
    
    # 2. Cargar Instructor
    with open('02_instructor.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            session.add(Instructor(
                id=int(fila['id']), 
                nombre=fila['nombre'].strip()
            ))
    print("[OK] 02_instructor.csv procesado.")
    session.commit() # Confirmamos los primeros maestros/catálogos independientes

    # 3. Cargar Curso
    with open('03_curso.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            session.add(Curso(
                id=int(fila['id']),
                titulo=fila['titulo'].strip(),
                departamento_id=int(fila['departamento_id']),
                instructor_id=int(fila['instructor_id'])
            ))
    print("[OK] 03_curso.csv procesado.")

    # 4. Cargar Estudiante
    with open('04_estudiante.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            session.add(Estudiante(
                id=int(fila['id']),
                nombre=fila['nombre'].strip()
            ))
    print("[OK] 04_estudiante.csv procesado.")
    session.commit() # Guardamos cursos y estudiantes antes de crear dependencias

    # 5. Cargar Inscripcion
    with open('05_inscripcion.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_ins = datetime.strptime(fila['fecha_inscripcion'].strip(), "%Y-%m-%d %H:%M:%S")
            session.add(Inscripcion(
                estudiante_id=int(fila['estudiante_id']),
                curso_id=int(fila['curso_id']),
                fecha_inscripcion=fecha_ins
            ))
    print("[OK] 05_inscripcion.csv procesado.")

    # 6. Cargar Tarea
    with open('06_tarea.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_ent = datetime.strptime(fila['fecha_entrega'].strip(), "%Y-%m-%d %H:%M:%S")
            session.add(Tarea(
                id=int(fila['id']),
                curso_id=int(fila['curso_id']),
                titulo=fila['titulo'].strip(),
                fecha_entrega=fecha_ent
            ))
    print("[OK] 06_tarea.csv procesado.")
    session.commit() # Guardamos para habilitar los IDs de las tareas

    # 7. Cargar Entrega
    with open('07_entrega.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_env = datetime.strptime(fila['fecha_envio'].strip(), "%Y-%m-%d %H:%M:%S")
            session.add(Entrega(
                id=int(fila['id']),
                tarea_id=int(fila['tarea_id']),
                estudiante_id=int(fila['estudiante_id']),
                fecha_envio=fecha_env,
                calificacion=float(fila['calificacion'])
            ))
    print("[OK] 07_entrega.csv procesado.")
    
    # Confirmar de forma definitiva todos los datos en la BD
    session.commit()
    print("\n¡Éxito! La base de datos ha sido poblada correctamente desde los archivos físicos.")

except FileNotFoundError as fnf_error:
    session.rollback()
    print(f"\n[ERROR]: No se pudo encontrar el archivo. Asegúrate de que esté en la misma carpeta: {fnf_error}")
except ValueError as val_error:
    session.rollback()
    print(f"\n[ERROR]: Error en la conversión de datos (revisa el formato de enteros o fechas): {val_error}")
except Exception as e:
    session.rollback()
    print(f"\n[ERROR]: Ocurrió un error inesperado al poblar la base de datos: {e}")
finally:
    session.close()
