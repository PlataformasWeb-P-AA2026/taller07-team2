# consulta2.py
from sqlalchemy.orm import sessionmaker
from clases import engine, Curso, Instructor

Session = sessionmaker(bind=engine)
session = Session()

print("CURSOS DICTADOS POR PROFESORES QUE CONTIENEN 'Zam'")
print("=" * 50)

# unimos con Instructor para poder filtrar por su nombre
cursos = session.query(Curso).join(Curso.instructor).filter(Instructor.nombre.like('%Zam%')).all()

for c in cursos:
    print(f"• Curso: '{c.titulo}' — Dictado por: {c.instructor.nombre} [{c.departamento.nombre}]")

session.close()
