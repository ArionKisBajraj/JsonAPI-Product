import mysql.connector

class DbManager:

    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None  # Aggiungiamo un attributo per la connessione

    def establish_connection(self):
        try:
            self.connection = mysql.connector.connect(  # Memorizziamo la connessione nell'attributo
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database
            )
            return self.connection
        except mysql.connector.Error as e:
            print("Errore di connessione al database:", str(e))

    def close_connection(self):  # Aggiungiamo un metodo per chiudere la connessione
        if self.connection:
            self.connection.close()
            print("Connessione chiusa.")
        else:
            print("Nessuna connessione attiva da chiudere.")

            print("Connessione al database chiusa.")



