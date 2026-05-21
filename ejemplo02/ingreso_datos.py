from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tablas import Club, Jugador

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Se procede a leer los CLUBES del .txt de la carpeta data para realizar el ingreso de datos a la base de datos
with open('./data/datos_clubs.txt', 'r', encoding='utf-8-sig') as f:
    for line in f:
        nombre, deporte, fundacion = line.strip().split(';')
        club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
        session.add(club)

# Guardamos los cambios en la base de datos
session.commit()

# Se procede a leer los JUGADORES del .txt de la carpeta data para realizar el ingreso de datos a la base de datos
with open('./data/datos_jugadores.txt', 'r', encoding='utf-8-sig') as f:
    for line in f:
        n_club, n_posicion, dorsal, nombre = line.strip().split(';')
        """
        Para obtener el objeto Club asociado al jugador, se realiza una consulta a la base de datos utilizando el nombre del club (n_club) leído del archivo.
        Se utiliza el método filter_by para filtrar los clubes por su nombre y el método first() para obtener el primer resultado de la consulta, que se espera sea el club correspondiente al jugador.
        """
        club_obj = session.query(Club).filter_by(nombre=n_club).first()

        jugador = Jugador(nombre=nombre, dorsal=int(dorsal), posicion=n_posicion, club=club_obj)
        session.add(jugador)

# Se guardan los cambios en la base de datos
session.commit()