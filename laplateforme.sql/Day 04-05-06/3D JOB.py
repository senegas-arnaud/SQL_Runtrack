import mysql.connector
from dotenv import load_dotenv
import os
import pygame
import sys

load_dotenv("c:/Users/arnau/Documents/La Plateforme/SQL/.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="store"
)
cursor = mydb.cursor()
pygame.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gestion des Stocks")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 24)

def fetch_products():
    cursor.execute("SELECT * FROM product")
    return cursor.fetchall()

def add_product(name, description, price, quantity, id_category):
    manage_data = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
    values = (name, description, price, quantity, id_category)
    cursor.execute(manage_data, values)
    mydb.commit()

def delete_product(product_id):
    manage_data = "DELETE FROM product WHERE id = %s"
    cursor.execute(manage_data, (product_id,))
    mydb.commit()

def update_product(product_id, field, new_value):
    manage_data = f"UPDATE product SET {field} = %s WHERE id = %s"
    cursor.execute(manage_data, (new_value, product_id))
    mydb.commit()

def product_exists(product_id):
    cursor.execute("SELECT id FROM product WHERE id = %s", (product_id,))
    return cursor.fetchone() is not None

def display_products(screen, products):
    y = 100
    for product in products:
        text = f"ID: {product[0]} | Nom: {product[1]} | Description: {product[2]} | Prix: {product[3]}€ | Stock: {product[4]} | Catégorie: {product[5]}"
        product_surface = font.render(text, True, BLACK)
        screen.blit(product_surface, (50, y))
        y += 30

def display_menu(screen, selected_option):
    options = ["Afficher tous les produits", "Ajouter un produit", "Supprimer un produit", "Modifier un produit"]
    y = 50
    for i, option in enumerate(options):
        color = BLUE if i == selected_option else BLACK
        option_surface = font.render(option, True, color)
        screen.blit(option_surface, (50, y))
        y += 40

def display_input_form(screen, fields, input_values, active_field):
    y = 300
    for i, field in enumerate(fields):
        label_surface = font.render(field, True, BLACK)
        screen.blit(label_surface, (50, y))
        input_surface = font.render(input_values[i], True, BLUE if i == active_field else BLACK)
        screen.blit(input_surface, (250, y))
        y += 40

def display_error(screen, message):
    error_surface = font.render(message, True, RED)
    screen.blit(error_surface, (50, 500))

def show_all_products(screen):
    products = fetch_products()
    running = True
    while running:
        screen.fill(WHITE)
        display_products(screen, products)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

def add_product_screen(screen):
    input_fields = ["Nom :", "Description :", "Prix :", "Quantité :", "ID Catégorie :"]
    input_values = [""] * len(input_fields)
    active_field = 0
    error_message = ""
    running = True

    while running:
        screen.fill(WHITE)
        display_input_form(screen, input_fields, input_values, active_field)
        if error_message:
            display_error(screen, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    return True
                elif event.key == pygame.K_TAB:  
                    active_field = (active_field + 1) % len(input_fields)
                elif event.key == pygame.K_BACKSPACE: 
                    input_values[active_field] = input_values[active_field][:-1]
                elif event.key == pygame.K_RETURN: 
                    try:
                        price = int(input_values[2])
                        quantity = int(input_values[3])
                        id_category = int(input_values[4])
                        add_product(input_values[0], input_values[1], price, quantity, id_category)
                        return True
                    except ValueError:
                        error_message = "Erreur : Prix, quantité ou ID catégorie invalide."
                else: 
                    input_values[active_field] += event.unicode

def delete_product_screen(screen):
    input_fields = ["ID du produit à supprimer :"]
    input_values = [""]
    active_field = 0
    error_message = ""
    running = True

    while running:
        screen.fill(WHITE)
        display_input_form(screen, input_fields, input_values, active_field)
        if error_message:
            display_error(screen, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    return True
                elif event.key == pygame.K_BACKSPACE: 
                    input_values[active_field] = input_values[active_field][:-1]
                elif event.key == pygame.K_RETURN: 
                    if input_values[0].isdigit() and product_exists(int(input_values[0])):
                        delete_product(int(input_values[0]))
                        return True
                    else:
                        error_message = "ID invalide ou produit inexistant."
                else:  
                    input_values[active_field] += event.unicode

def update_product_screen(screen):
    input_fields = ["ID du produit à modifier :", "Champ à modifier :", "Nouvelle valeur :"]
    input_values = [""] * len(input_fields)
    active_field = 0
    error_message = ""
    running = True

    while running:
        screen.fill(WHITE)
        display_input_form(screen, input_fields, input_values, active_field)
        if error_message:
            display_error(screen, error_message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    return True
                elif event.key == pygame.K_TAB: 
                    active_field = (active_field + 1) % len(input_fields)
                elif event.key == pygame.K_BACKSPACE: 
                    input_values[active_field] = input_values[active_field][:-1]
                elif event.key == pygame.K_RETURN: 
                    if input_values[0].isdigit() and product_exists(int(input_values[0])):
                        update_product(int(input_values[0]), input_values[1], input_values[2])
                        return True
                    else:
                        error_message = "ID invalide ou produit inexistant."
                else:
                    input_values[active_field] += event.unicode

def main():
    running = True
    selected_option = 0

    while running:
        screen.fill(WHITE)
        display_menu(screen, selected_option)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  
                    selected_option = (selected_option - 1) % 4
                elif event.key == pygame.K_DOWN: 
                    selected_option = (selected_option + 1) % 4
                elif event.key == pygame.K_RETURN: 
                    if selected_option == 0:  
                        running = show_all_products(screen)
                    elif selected_option == 1: 
                        running = add_product_screen(screen)
                    elif selected_option == 2: 
                        running = delete_product_screen(screen)
                    elif selected_option == 3: 
                        running = update_product_screen(screen)

    pygame.quit()
    cursor.close()
    mydb.close()
    sys.exit()

main()

#add_category("electronique")
#add_category("vetements")
#add_category("alimentation")
#add_category("meubles")
#add_category("livre")
#mydb.commit()

#add_product("Téléphone", "Smartphone Android", 300, 10, 1)
#add_product("Casque Audio", "Casque sans fil", 50, 15, 1)
#add_product("Laptop", "Ordinateur portable", 800, 5, 1)
#add_product("T-shirt", "T-shirt en coton", 20, 30, 2)
#add_product("Jeans", "Jeans slim", 40, 25, 2)
#add_product("Chaussures", "Chaussures en cuir", 60, 20, 2),
#add_product("Pomme", "Pomme de saison", 2, 100, 3), 
#add_product("Pain", "Pain frais", 1, 200, 3),
#add_product("Bananes", "Bananes bio", 3, 150, 3),
#add_product("Table", "Table en bois", 150, 10, 4), 
#add_product("Chaise", "Chaise en plastique", 25, 30, 4),
#add_product("Armoire", "Armoire à deux portes", 120, 8, 4),
#add_product("Roman", "Roman historique", 15, 50, 5),
#add_product("Science Fiction", "Livre de science fiction", 18, 40, 5),
#add_product("Livre de cuisine", "Recettes simples", 25, 20, 5),
#add_product("Bande dessinée", "BD humoristique", 12, 60, 5),
#add_product("Guide de voyage", "Voyages en Europe", 20, 35, 5),
#add_product("Encyclopédie", "Encyclopédie générale", 60, 10, 5),
#add_product("Cahier", "Cahier à spirale", 5, 80, 5)
