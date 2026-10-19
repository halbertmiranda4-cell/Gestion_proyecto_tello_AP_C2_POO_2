from peewee import MySQLDatabase
from decouple import config


def conectar_db():
    # Todas las credenciales vienen del archivo .env (que NO se sube a GitHub)
    base_datos = MySQLDatabase(config('DB_NAME'),
                               **{
                                   'charset': 'utf8mb4',
                                   'host': config('DB_HOST', default='localhost'),
                                   'port': config('DB_PORT', cast=int, default=3306),
                                   'user': config('DB_USER'),
                                   'password': config('DB_PASSWORD')})
    return base_datos 