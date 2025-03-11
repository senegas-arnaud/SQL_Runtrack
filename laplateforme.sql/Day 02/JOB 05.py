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

cursor.execute("SELECT SUM(superficie) FROM etage")
superficie = cursor.fetchall()
totale = int(superficie[0][0])

print(f"La superficie de La Plateforme est de {totale} m2")




cursor.close()
mydb.close()