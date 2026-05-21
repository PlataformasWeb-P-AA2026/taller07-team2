from config import cadena_base_datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from clases import Curso, Tarea 

# configuracion de la sesión
engine = create_engine(cadena_base_datos)
Session = sessionmaker(bind=engine)
session = Session()

# traer cursos y sus tareas
cursos = session.query(Curso).options(joinedload(Curso.tareas)).all()

# presentacion de datos estándar y directa
for curso in cursos:
    print("curso:", curso.titulo)
    
    if curso.tareas:
        for tarea in curso.tareas:
            print("  -tarea:", tarea.titulo, "| fecha de entrega:", tarea.fecha_entrega)
    else:
        print("no hay tareas asociadas")
    print() # Línea en blanco para separar cada curso

session.close()
