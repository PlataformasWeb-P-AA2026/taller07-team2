# consulta3.py
from sqlalchemy.orm import sessionmaker
from clases import engine, Inscripcion, Curso, Departamento

Session = sessionmaker(bind=engine)
session = Session()

print("INSCRIPCIONES EN EL DEPARTAMENTO DE CIENCIAS DE LA COMPUTACIÓN")
print("=" * 60)
#cruzamos las relaciones necesarias para llegar al nombre del departamento y filtrar
inscripciones = session.query(Inscripcion)\
    .join(Inscripcion.curso)\
    .join(Curso.departamento)\
    .filter(Departamento.nombre == 'Ciencias de la Computación')\
    .all()

for i in inscripciones:
    #extramoe las variables usando las relaciones del ORM
    estudiante = i.estudiante.nombre
    curso = i.curso.titulo
    profesor = i.curso.instructor.nombre
    
    print(f"• {estudiante} se inscribió en '{curso}' (Profesor/a: {profesor})")

session.close()
