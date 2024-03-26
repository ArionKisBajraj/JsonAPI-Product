document.addEventListener("DOMContentLoaded", function() {
    // Costante per l'URL delle API
    const apiUrl = "//home/kisbajrajarion/Scaricati/JsonAPI-Product-main/JsonAPI-Product/PY_script";

    // Bottone "Crea" per aprire il form modale
    const createButton = document.getElementById("createButton");
    createButton.addEventListener("click", function() {
        // Cancella il contenuto del form modale
        const modalContent = document.querySelector("#productModal .modal-content");
        modalContent.innerHTML = "";
        console.log("Bottone premuto")

        // Aggiungi il form di creazione al form modale
        const formHTML = `
            <div class="modal-header">
                <h5 class="modal-title" id="productModalLabel">Crea Prodotto</h5>
                <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <!-- Qui inserisci il form di creazione -->
                <form>
                    <div class="mb-3">
                        <label for="marca" class="form-label">Marca</label>
                        <input type="text" class="form-control" id="marca">
                    </div>
                    <div class="mb-3">
                        <label for="modello" class="form-label">Modello</label>
                        <input type
                        ="text" class="form-control" id="modello">
                        </div>
                        <div class="mb-3">
                            <label for="prezzo" class="form-label">Prezzo</label>
                            <input type="text" class="form-control" id="prezzo">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Annulla</button>
                    <button type="button" class="btn btn-primary" id="saveButton">Salva</button>
                </div>
            `;
            modalContent.innerHTML = formHTML;
    
            // Visualizza il modal
            const productModal = new bootstrap.Modal(document.getElementById('productModal'));
            productModal.show();
        });
    
        // Funzione per ottenere la lista dei prodotti
        function getProducts() {
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    const productList = document.getElementById("productList");
                    productList.innerHTML = "";
                    data.forEach(product => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${product.id}</td>
                            <td>${product.marca}</td>
                            <td>${product.modello}</td>
                            <td>${product.prezzo}</td>
                            <td>
                                <button class="btn btn-primary" onclick="showProductDetails(${product.id})">Show</button>
                                <button class="btn btn-secondary" onclick="editProduct(${product.id})">Edit</button>
                                <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                            </td>
                        `;
                        productList.appendChild(row);
                    });
                })
                .catch(error => console.error("Error fetching products:", error));
        }
    
        // Chiama la funzione per ottenere la lista dei prodotti al caricamento della pagina
        getProducts();
    });
    