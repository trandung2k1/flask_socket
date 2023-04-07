import mysql.connector
from dotenv import dotenv_values
config = dotenv_values(".env")
MyDB = mysql.connector.connect(
    host=config['HOST'],
    user=config['USER'],
    password=config['PASSWORD'],
    port=config['PORTDB'],
    database=config['DATABASE']
)
