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
    
    # Confirmamos los primeros maestros para poder consultarlos en las siguientes inserciones
    session.commit() 

    # 3. Cargar Curso
    with open('03_curso.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            # Consultamos los objetos Departamento e Instructor por su ID
            dep_obj = session.query(Departamento).filter_by(id=int(fila['departamento_id'])).first()
            inst_obj = session.query(Instructor).filter_by(id=int(fila['instructor_id'])).first()
            
            session.add(Curso(
                id=int(fila['id']),
                titulo=fila['titulo'].strip(),
                departamento=dep_obj, # Enviamos el objeto en lugar del ID
                instructor=inst_obj   # Enviamos el objeto en lugar del ID
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
    
    # Guardamos cursos y estudiantes antes de crear dependencias
    session.commit() 

    # 5. Cargar Inscripcion
    with open('05_inscripcion.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_ins = datetime.strptime(fila['fecha_inscripcion'].strip(), "%Y-%m-%d %H:%M:%S")
            
            # Consultamos los objetos Estudiante y Curso
            est_obj = session.query(Estudiante).filter_by(id=int(fila['estudiante_id'])).first()
            cur_obj = session.query(Curso).filter_by(id=int(fila['curso_id'])).first()
            
            session.add(Inscripcion(
                estudiante=est_obj, # Enviamos el objeto
                curso=cur_obj,      # Enviamos el objeto
                fecha_inscripcion=fecha_ins
            ))
    print("[OK] 05_inscripcion.csv procesado.")

    # 6. Cargar Tarea
    with open('06_tarea.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_ent = datetime.strptime(fila['fecha_entrega'].strip(), "%Y-%m-%d %H:%M:%S")
            
            # Consultamos el objeto Curso
            cur_obj = session.query(Curso).filter_by(id=int(fila['curso_id'])).first()
            
            session.add(Tarea(
                id=int(fila['id']),
                curso=cur_obj, # Enviamos el objeto
                titulo=fila['titulo'].strip(),
                fecha_entrega=fecha_ent
            ))
    print("[OK] 06_tarea.csv procesado.")
    
    # Guardamos para habilitar los IDs de las tareas
    session.commit() 

    # 7. Cargar Entrega
    with open('07_entrega.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            fecha_env = datetime.strptime(fila['fecha_envio'].strip(), "%Y-%m-%d %H:%M:%S")
            
            # Consultamos los objetos Tarea y Estudiante
            tar_obj = session.query(Tarea).filter_by(id=int(fila['tarea_id'])).first()
            est_obj = session.query(Estudiante).filter_by(id=int(fila['estudiante_id'])).first()
            
            session.add(Entrega(
                id=int(fila['id']),
                tarea=tar_obj,       # Enviamos el objeto
                estudiante=est_obj,  # Enviamos el objeto
                fecha_envio=fecha_env,
                calificacion=float(fila['calificacion'])
            ))
    print("[OK] 07_entrega.csv procesado.")
    
    # Confirmar de forma definitiva todos los datos en la BD
    session.commit()
    print("\n¡Éxito! La base de datos ha sido poblada correctamente utilizando la asignación por objetos.")

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