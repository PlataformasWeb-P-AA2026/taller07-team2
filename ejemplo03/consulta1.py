# consulta1.py
from sqlalchemy.orm import sessionmaker
from clases import engine, Entrega

Session = sessionmaker(bind=engine)
session = Session()

print("LISTADO DE ENTREGAS")
print("=" * 20)

entregas = session.query(Entrega).all()
for e in entregas:
    #acceso mediante las relaciones del ORM
    nombre_estudiante = e.estudiante.nombre
    titulo_tarea = e.tarea.titulo 
    nombre_profesor = e.tarea.curso.instructor.nombre
    
    # Formato natural: Estudiante mandó 'Tarea' (Profesor: Nombre)
    print(f"• {nombre_estudiante} entregó '{titulo_tarea}' — [Profesor/a: {nombre_profesor}]")

session.close()
