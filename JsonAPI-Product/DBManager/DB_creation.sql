create database DBproducts;
CREATE TABLE DBproducts.products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    prezzo float NOT NULL
);


