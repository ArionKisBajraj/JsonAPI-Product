from DB_connection import DbManager
import mysql.connector

class Product:

    @staticmethod
    def connection():
        try:
            db_manager = DbManager("192.168.2.200", 3306, "kisbajraj_arion", "vizier.Dunant.fisheries.", "kisbajraj_arion_DBproducts") 
            return db_manager.establish_connection()
        except mysql.connector.Error as e:
            print("Errore durante la connessione al database:", str(e))

    def __init__(self, id, nome, prezzo, marca):
        self._id = id
        self._nome = nome
        self._prezzo = prezzo
        self._marca = marca
    
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def prezzo(self):
        return self._prezzo

    @property
    def marca(self):
        return self._marca

    @staticmethod
    def fetchAll():
        try: 
            conn = Product.connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM products")
            records = cursor.fetchall()
            cursor.close()
            return records
        except mysql.connector.Error as e:
            print("Errore durante la ricerca dei prodotti:", str(e))

    @staticmethod
    def find_id(id):
        try:
            conn = Product.connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return dict(id=row[0], marca=row[1], nome=row[2], prezzo=row[3])
            else:
                return None
        except mysql.connector.Error as e:
            print("Errore durante la ricerca del prodotto:", str(e))
    def find_id_product(id):
        try:
            conn = Product.connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return Product(id=row[0], marca=row[1], nome=row[2], prezzo=row[3])
            else:
                return None
        except mysql.connector.Error as e:
            print("Errore durante la ricerca del prodotto:", str(e))
    

    @staticmethod
    def create_product(product_data):
        try:
            conn = Product.connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (nome, prezzo, marca) VALUES (%s, %s, %s)", (product_data['nome'], product_data['prezzo'], product_data['marca']))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            product_data['id'] = product_id
            return product_data
        except mysql.connector.Error as e:
            print("Errore durante la creazione del prodotto:", str(e))

    def update_product(self, product_data):
        try:
            conn = Product.connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET marca = %s, nome = %s, prezzo = %s WHERE id = %s", (product_data['marca'], product_data['nome'], product_data['prezzo'], self.id,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print("Errore durante l'aggiornamento del prodotto:", str(e))

    def delete_product(self):
        try:
            conn = Product.connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (self.id,))
            conn.commit()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print("Errore durante l'eliminazione del prodotto:", str(e))
            return False
