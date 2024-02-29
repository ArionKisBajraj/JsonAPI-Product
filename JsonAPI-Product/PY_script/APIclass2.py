# APIclass.py

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from Products import Product

class RequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/products':
            self._handle_get_products()
        elif self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            self._handle_get_product(product_id)
        else:
            self.send_error(404, 'Not Found')

    def _handle_get_products(self):
        records = Product.fetchAll()
        products_list = []
        for record in records:
            product_dict = self._format_product(record)
            products_list.append(product_dict)

        self._set_response()
        response_data = {'data': products_list}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def _handle_get_product(self, product_id):
        product = Product.find_id(product_id)
        if product is not None:
            product_dict = self._format_product(product)
            response_data = {'data': product_dict}
            self._set_response()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, 'Product Not Found')

    def _format_product(self, product):
        if isinstance(product, dict):
            return {
                'type': 'products',
                'id': product.get('id', ''),
                'attributes': {
                    'marca': product.get('marca', ''),
                    'nome': product.get('nome', ''),
                    'prezzo': product.get('prezzo', '')
                }
            }
        else:
            raise TypeError("Dovrebbe essere un dict")

    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self._handle_create_product(post_data)
        else:
            self.send_error(404, 'Not Found')

    def _handle_create_product(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            if 'data' not in data or 'attributes' not in data['data']:
                self.send_error(400, 'Bad Request - Incomplete Data Request')
                

            attributes = data['data']['attributes']
            new_product = {
                'nome': attributes.get('nome', ''),
                'prezzo': attributes.get('prezzo', 0),
                'marca': attributes.get('marca', '')
            }
            product = Product.create_product(new_product)
            product_dict = self._format_product(product)

            self._set_response(status_code=201)
            response_data = {'data': product_dict}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, 'Bad Request - Invalid JSON')

    def do_DELETE(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Product.find_id_product(product_id)
            self._handle_delete_product(product)
            
        else:
            self.send_error(404, 'Not Found')

    def _handle_delete_product(self, product):
        try:
     
            if product:
                if product.delete_product():
                  self._set_response(status_code=204)  # No Content
                else:
                  self.send_error(500, 'Failed to delete product')
            else:
            # Se il prodotto non esiste, restituisce uno stato 404 (Not Found)
                self.send_error(404, 'Product Not Found')
        except Exception as e:
        # In caso di errore interno, restituisce uno stato 500 (Internal Server Error)
            self.send_error(500, f'Internal Server Error: {str(e)}')

    def do_PATCH(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Product.find_id(product_id)
            if product:
                content_length = int(self.headers['Content-Length'])
                patch_data = self.rfile.read(content_length)
                self._handle_patch_product(product, patch_data)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')

    def _handle_patch_product(self, product, patch_data):
        try:
            data = json.loads(patch_data.decode('utf-8'))
            if 'data' not in data or 'attributes' not in data['data']:
                self.send_error(400, 'Bad Request - Incomplete Data Request')
            attributes = data['data']['attributes']
            for key, value in attributes.items():
                if key in product:
                    product[key] = value
            self._set_response()
            response_data = {'data': self._format_product(product)}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, 'Bad Request - Invalid JSON')       

if __name__ == '__main__':
    server_address = ('192.168.2.216', 8081)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port 8081...')
    httpd.serve_forever()
    




