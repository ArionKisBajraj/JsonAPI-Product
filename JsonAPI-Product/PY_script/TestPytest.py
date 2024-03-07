import pytest
from Products import Product  


@pytest.fixture(scope="module")
def product_instance():
    # Creazione di un prodotto di esempio per i test
    product_data = {'nome': 'Prodotto di esempio', 'prezzo': 10.0, 'marca': 'Marca di esempio'}
    product = Product.create_product(product_data)
    yield product
    # Alla fine dei test, eliminiamo il prodotto di esempio
    Product.delete_product(product.id)

def test_fetchAll(product_instance):
    # Verifica se fetchAll restituisce dei risultati non vuoti
    records = Product.fetchAll()
    assert records

def test_find_id(product_instance):
    # Verifica se find_id restituisce un risultato non nullo per un id valido
    product = Product.find_id(product_instance.id)
    assert product is not None

def test_find_id_product(product_instance):
    # Verifica se find_id_product restituisce un'istanza di Product per un id valido
    product = Product.find_id_product(product_instance.id)
    assert isinstance(product, Product)

def test_create_product():
    # Verifica se create_product crea correttamente un nuovo prodotto
    new_product_data = {'nome': 'Nuovo prodotto', 'prezzo': 20.0, 'marca': 'Nuova marca'}
    created_product = Product.create_product(new_product_data)
    assert created_product is not None

def test_update_product(product_instance):
    # Verifica se update_product aggiorna correttamente un prodotto esistente
    updated_product_data = {'id': product_instance.id, 'nome': 'Prodotto aggiornato', 'prezzo': 15.0, 'marca': 'Marca aggiornata'}
    Product.update_product(updated_product_data)
    updated_product = Product.find_id_product(product_instance.id)
    assert updated_product.nome == 'Prodotto aggiornato'
    assert updated_product.prezzo == 15.0
    assert updated_product.marca == 'Marca aggiornata'

def test_delete_product(product_instance):
    # Verifica se delete_product elimina correttamente un prodotto esistente
    deleted = Product.delete_product(product_instance.id)
    assert deleted
