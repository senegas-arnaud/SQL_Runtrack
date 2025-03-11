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
    database = "Zoo"
)

cursor = mydb.cursor()

cursor.execute("DROP TABLE cage")
mydb.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cage (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    superficie INT,
    capacite INT
);
""")

mydb.commit()
 
cursor.execute("""
CREATE TABLE IF NOT EXISTS animal (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nom VARCHAR(255) NOT NULL,
    race VARCHAR(255) NOT NULL,
    id_cage INT,
    date DATE,
    pays VARCHAR(255) NOT NULL
);
""")

mydb.commit()

def add_animal(nom, race, id_cage, date, pays):
    cursor.execute("SELECT capacite FROM cage WHERE id = %s", (id_cage,))
    result = cursor.fetchone()
    if result:
        capacite_cage = result[0]
        cursor.execute("SELECT COUNT(*) FROM animal WHERE id_cage = %s", (id_cage,))
        nombre_animaux = cursor.fetchone()[0]
        
        if nombre_animaux >= capacite_cage:
            print(f"La cage avec l'id {id_cage} est pleine. Impossible d'ajouter {nom} {race}.")
        else:
            manage_data = "INSERT INTO animal (nom, race, id_cage, date, pays) VALUES (%s, %s, %s, %s, %s)"
            value = (nom, race, id_cage, date, pays)
            cursor.execute(manage_data, value)
            mydb.commit()
            print(f"Vous avez ajouté {nom} {race} à la cage {id_cage}.")
    else:
        print(f"Aucune cage trouvée avec l'ID {id_cage}.")

def add_cage(superficie, capacite):
    manage_data = "INSERT INTO cage (superficie, capacite) VALUES (%s, %s)"
    value = (superficie, capacite)
    cursor.execute(manage_data,value)
    mydb.commit()
    print(f"Vous avez ajouté une cage de superficie {superficie}m² et de capacité {capacite}")

def del_animal(nom, race):
    manage_data = "DELETE FROM animal WHERE nom = %s AND race = %s"
    value = (nom , race)
    cursor.execute(manage_data, value)
    mydb.commit()
    print(f"Animal {nom} {race} supprimé")

def del_cage(superficie, capacite):
    manage_data = "DELETE FROM cage WHERE nom = %s AND prenom = %s"
    value = (superficie, capacite)
    cursor.execute(manage_data, value)
    mydb.commit()
    print(f"Cage de superficie {superficie}m² et de capacité {capacite} supprimé")

def affiche_animaux():
    cursor.execute("SELECT nom, race, id_cage, date, pays FROM animal")
    animaux = cursor.fetchall()
    for animal in animaux:
        print(f"Nom : {animal[0]}, Race : {animal[1]}, Cage ID : {animal[2]}, Date : {animal[3]}, Pays : {animal[4]}")



def affiche_cage():
    cursor.execute("SELECT id, superficie, capacite FROM cage")
    cages = cursor.fetchall()
    for cage in cages:
        cage_id = cage[0]
        superficie = cage[1]
        capacite = cage[2]
        print(f"\nCage ID : {cage_id} (Superficie : {superficie} m², Capacité : {capacite} animaux)")
            
        cursor.execute("SELECT nom, race FROM animal WHERE id_cage = %s", (cage_id,))
        animaux_cage = cursor.fetchall()
            
        if animaux_cage:
            for animal in animaux_cage:
                print(f"  - {animal[0]} ({animal[1]})")
        if animaux_cage == 0 :
            print("Cette cage est vide")


def superficie_totale():
    cursor.execute("SELECT SUM(superficie) FROM cage")
    superfi = cursor.fetchall()
    if superfi[0][0] is None:
        totale = 0
    else:
        totale = int(superfi[0][0])
    print(f"La superficie totale de toutes les cages est de {totale}m²")



add_cage(20,1)
add_cage(40,2)
add_cage(60,3)
add_cage(80,4)
mydb.commit()
#add_animal("Simba", "Lion", 1,"2025-03-11" , "Kenya")
#add_animal("Zizou", "Zebre", 2,"2025-03-11" , "Tanzanie")
#add_animal("Zazou", "Zebre", 2, "2025-03-11", "Tanzanie")
#add_animal("Zizi", "Zebre", 2, "2025-03-11", "Tanzanie")
#add_animal("Gigi", "Giraffe", 3, "2025-03-11", "Kenya")
#mydb.commit()
#del_animal("Gigi","Giraffe")
mydb.commit()


affiche_animaux()
affiche_cage()
superficie_totale()


cursor.close()
mydb.close()
