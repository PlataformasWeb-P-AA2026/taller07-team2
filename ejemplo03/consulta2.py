# consulta2.py
from sqlalchemy.orm import sessionmaker
from clases import engine, Curso, Instructor

Session = sessionmaker(bind=engine)
session = Session()

print("CURSOS DICTADOS POR PROFESORES QUE CONTIENEN 'Zam'")
print("=" * 50)

# se uno instructor para poder filtrar por su nombre
cursos = session.query(Curso).join(Curso.instructor).filter(Instructor.nombre.like('%Zam%')).all()

if not cursos:
    print("no se encontraron cursos con ese criterio.")
else:
    for c in cursos:
        # Formato natural: Título del curso (Profesor: Nombre) [Departamento: Nombre]
        print(f"• Curso: '{c.titulo}' — Dictado por: {c.instructor.nombre} [{c.departamento.nombre}]")

session.close()
