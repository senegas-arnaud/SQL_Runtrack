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

cursor.execute("""
CREATE TABLE IF NOT EXISTS etage (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nom VARCHAR(255) NOT NULL,
    numero INT,
    superficie INT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS salle (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nom VARCHAR(255) NOT NULL,
    id_etage INT,
    capacite INT
);
""")

mydb.commit()

cursor.execute("SHOW TABLES")

result = cursor.fetchall()
print(result)

cursor.execute("INSERT INTO etage (nom, numero, superficie) VALUES ('RDC' , 0 ,  500);")
cursor.execute("INSERT INTO etage (nom, numero, superficie) VALUES ('R+1' , 1 ,  500);")

cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Lounge', 1 , 100);")
cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Studio Son', 1 , 5);")
cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Broadcasting', 2 , 5);")
cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Bocal Peda', 2 , 4);")
cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Coworking', 2 , 80);")
cursor.execute("INSERT INTO salle (nom, id_etage, capacite) VALUES ('Studio Video', 2 , 5);")
mydb.commit()


cursor.execute("SELECT * FROM etage")
result_etage = cursor.fetchall()
print(result_etage)

cursor.execute("SELECT * FROM salle")
result_salle = cursor.fetchall()
print(result_salle)

cursor.close()
mydb.close()