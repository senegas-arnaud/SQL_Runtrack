import mysql.connector
from dotenv import load_dotenv
import os



# Charger les variables d'environnement depuis le fichier .env
load_dotenv("c:/Users/arnau/Documents/La Plateforme/SQL/.env")

#Permet de se connecter a la base de donnée
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = os.getenv("PASSWORD"),
    database = "LaPlateforme",
)

cursor = mydb.cursor()

cursor.execute("SELECT nom, capacite FROM salle ")
result = cursor.fetchall()
print(result)



cursor.close()
mydb.close()