import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from product import Product

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
        records = Product.fetch_all()
        products_list = []
        for record in records:
            product_dict = self._format_product(record)
            products_list.append(product_dict)

        self._set_response()
        response_data = {'data': products_list}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def _handle_get_product(self, product_id):
        product = Product.find(product_id)
        if product is not None:
            product_dict = self._format_product(product)
            self._set_response()
            response_data = {'data': product_dict}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, 'Product Not Found')

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
                return

            attributes = data['data']['attributes']
            new_product = {
                'nome': attributes.get('nome', ''),
                'prezzo': attributes.get('prezzo', 0),
                'marca': attributes.get('marca', '')
            }
            product = Product.create(new_product)
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
            product = Product.find(product_id)
            if product:
                self._handle_delete_product(product)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')

    def _handle_delete_product(self, product):
        try:
            product.delete()
            self._set_response(status_code=204)  # No Content
        except Exception as e:
            self.send_error(500, f'Internal Server Error: {str(e)}')

    def _format_product(self, product):
        return {
            'type': 'products',
            'id': str(product.id),
            'attributes': {
                'marca': product.marca,
                'nome': product.nome,
                'prezzo': str(product.prezzo)
            }
        }

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
