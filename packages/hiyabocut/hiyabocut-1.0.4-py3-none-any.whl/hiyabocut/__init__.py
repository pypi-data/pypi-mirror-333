#import sqlite3
import random
import string
import mysql.connector

def generar_cadena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def short(enlace_largo):
    """Acorta un enlace largo generando un enlace corto único."""
    try:
        with mysql.connector.connect(
            host="mysql-hiyabopro.alwaysdata.net",
            user="hiyabopro_db",
            password="Informatur26*",
            database="hiyabopro_db"
        ) as conn:
            with conn.cursor() as c:
                # Crear la tabla si no existe
                c.execute('''CREATE TABLE IF NOT EXISTS enlaces (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    enlace_largo TEXT NOT NULL,
                    enlace_corto VARCHAR(255) NOT NULL UNIQUE
                )''')

                # Verificar si ya existe un enlace corto para ese enlace largo
                c.execute("SELECT enlace_corto FROM enlaces WHERE enlace_largo = %s", (enlace_largo,))
                resultado = c.fetchone()
                if resultado:
                    return resultado[0]

                # Generar y almacenar un nuevo enlace corto
                while True:
                    enlace_corto = generar_cadena_aleatoria()
                    try:
                        c.execute("INSERT INTO enlaces (enlace_largo, enlace_corto) VALUES (%s, %s)", 
                                  (enlace_largo, enlace_corto))
                        conn.commit()
                        return enlace_corto
                    except mysql.connector.IntegrityError:
                        continue  # Enlace duplicado, genera otro

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None

def unshort(enlace_corto):
    """Devuelve el enlace largo a partir del enlace corto."""
    try:
        with mysql.connector.connect(
            host="mysql-hiyabopro.alwaysdata.net",
            user="hiyabopro_db",
            password="Informatur26*",
            database="hiyabopro_db"
        ) as conn:
            with conn.cursor() as c:
                c.execute("SELECT enlace_largo FROM enlaces WHERE enlace_corto = %s", (enlace_corto,))
                resultado = c.fetchone()
                return resultado[0] if resultado else None

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None