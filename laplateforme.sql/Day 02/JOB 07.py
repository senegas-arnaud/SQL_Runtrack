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
    database = "new_database"
)

cursor = mydb.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS service (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nom VARCHAR(255) NOT NULL
);
""")

mydb.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employe (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    salaire DECIMAL,
    id_service INT
);
""")

mydb.commit()

cursor.execute("INSERT INTO service (nom) VALUES ('CEO');")
cursor.execute("INSERT INTO service (nom) VALUES ('Alternant');")
mydb.commit()

cursor.execute("INSERT INTO employe (nom, prenom, salaire, id_service) VALUES ('Senegas' , 'Arnaud' ,  5000 , 1);")
cursor.execute("INSERT INTO employe (nom, prenom, salaire, id_service) VALUES ('Doe' , 'John' ,  1500 , 2);")
mydb.commit()

cursor.execute("SELECT * FROM employe")
result = cursor.fetchall()
print(result)

cursor.execute("SELECT * FROM employe WHERE salaire > 3000")
big_salary = cursor.fetchall()
print(big_salary)

cursor.execute("""
SELECT employe.nom, employe.prenom, employe.salaire, service.nom AS service
FROM employe
JOIN service ON employe.id_service = service.id
""")
info = cursor.fetchall()
print(info)


cursor.close()
mydb.close()


class Employe : 
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("PASSWORD"),
            database="new_database"
        )
        self.cursor = self.mydb.cursor()

    def new_employe(self, nom, prenom, salaire, id_service):
        manage_data = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        value = (nom, prenom, salaire, id_service)
        self.cursor.execute(manage_data,value)
        self.mydb.commit()
        print(f"Vous avez ajouté {nom}{prenom} à vos employés")

    def delete_employe_name(self, nom, prenom):
        manage_data = "DELETE FROM employe WHERE nom = %s AND prenom = %s"
        value = (nom , prenom)
        self.cursor.execute(manage_data, value)
        self.mydb.commit()
        print(f"Employé {nom} {prenom} à été viré")

    def delete_ID(self, id_employe):
        manage_data = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(manage_data, (id_employe,))
        self.mydb.commit()
        print(f"Employé avec ID {id_employe} viré")

    def read_all(self):
        manage_data = """
        SELECT employe.nom, employe.prenom, employe.salaire, service.nom AS service
        FROM employe
        JOIN service ON employe.id_service = service.id
        """
        self.cursor.execute(manage_data)
        show_all = self.cursor.fetchall()
        print(show_all)


employe = Employe()
employe.new_employe("Guy","Jean",1800,2)
employe.delete_employe_name("Guy","Jean")
employe.read_all()

