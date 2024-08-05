from flask import Flask, render_template_string, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

# Utilizar la instancia de app desde app.py
from app import app

app = Flask(__name__)

class MongoDBConnection:
    def __init__(self, uri='mongodb+srv://msolano80258:Francia9192@cluster0.6uxqadh.mongodb.net/?retryWrites=true&w=majority'):
        try:
            self.client = MongoClient(uri)
            self.db = self.client['ProyectoNosql']
            print("Conexión a MongoDB exitosa")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

@app.route('/')
def index():
    try:
        db_connection = MongoDBConnection()
        property_collection = db_connection.get_collection('Property')
        properties = property_collection.find()

        property_list = []
        for property in properties:
            image_urls = property.get('images', ['static/images/placeholder.jpg'])
        # Crear una instancia de MongoDBConnection
        db_connection = MongoDBConnection()

        # Seleccionar la colección de propiedades
        property_collection = db_connection.get_collection('Property')

        # Realizar una consulta simple (ejemplo: obtener todas las propiedades)
        properties = property_collection.find()  # Sin limitación en el número de propiedades

        # Preparar datos para mostrar propiedades
        property_list = []
        for property in properties:
            # Obtener las imágenes asociadas a la propiedad
            image_urls = property.get('images', ['static/images/placeholder.jpg'])

            property_list.append({
                'name': property.get('name', 'Nombre de la Propiedad'),
                'price': property.get('price', '0'),
                'transaction_type': property.get('transaction_type', 'Tipo de Transacción'),
                'antiquity': property.get('antiquity', 'Antigüedad'),
                'owner': property.get('owner', 'Propietario'),
                'images': image_urls,
                'id': str(property.get('_id'))
            })

        db_connection.close()


        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Bienes Raíces</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                header {
                    background-color: #007BFF;
                    color: #fff;
                    padding: 1rem 0;
                    text-align: center;
                }
                .container {
                    width: 80%;
                    margin: 0 auto;
                    overflow: hidden;
                }
                .property {
                    background: #fff;
                    margin: 1rem 0;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    display: flex;
                    flex-direction: column;
                }
                .property-info {
                    display: flex;
                    flex-direction: column;
                }
                .property-images {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                .property-images img {
                    width: 100px;
                    height: 75px;
                    object-fit: cover;
                    border-radius: 8px;
                }
                .property-info h2 {
                    margin-top: 0;
                }
                .property-info a {
                    text-decoration: none;
                    color: #007BFF;
                }
                footer {
                    background-color: #333;
                    color: #fff;
                    text-align: center;
                    padding: 1rem 0;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Bienes Raíces</h1>
                </div>
            </header>
            <div class="container">
                <h2>Propiedades Destacadas</h2>
                <div class="properties">
                    {% for property in properties %}
                    <div class="property">
                        <div class="property-info">
                            <h2>{{ property.name }}</h2>
                            <p><strong>Precio:</strong> ${{ property.price }}</p>
                            <p><strong>Tipo de Transacción:</strong> {{ property.transaction_type }}</p>
                            <p><strong>Años de Antigüedad:</strong> {{ property.antiquity }}</p>
                            <p><strong>Propietario:</strong> {{ property.owner }}</p>
                            <div class="property-images">
                                {% for image in property.images %}
                                <img src="{{ image }}" alt="Imagen de la propiedad">
                                {% endfor %}
                            </div>
                            <a href="{{ url_for('details', property_id=property.id) }}">Ver más</a>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <footer>
                <p>&copy; 2024 Bienes Raíces. Todos los derechos reservados.</p>
            </footer>
        </body>
        </html>
        """

        # HTML con el contenido embebido
        html = """
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bienes Raíces</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #007BFF;
            color: #fff;
            padding: 1rem 0;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            overflow: hidden;
        }
        .property {
            background: #fff;
            margin: 1rem 0;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        .property-info {
            display: flex;
            flex-direction: column;
        }
        .property-images {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .property-images img {
            width: 100px;
            height: 75px;
            object-fit: cover;
            border-radius: 8px;
        }
        .property-info h2 {
            margin-top: 0;
        }
        .property-info a {
            text-decoration: none;
            color: #007BFF;
        }
        footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 1rem 0;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Bienes Raíces</h1>
        </div>
    </header>
    <div class="container">
        <h2>Propiedades Destacadas</h2>
        <div class="properties">
            {% for property in properties %}
            <div class="property">
                <div class="property-info">
                    <h2>{{ property.name }}</h2>
                    <p><strong>Precio:</strong> ${{ property.price }}</p>
                    <p><strong>Tipo de Transacción:</strong> {{ property.transaction_type }}</p>
                    <p><strong>Años de Antigüedad:</strong> {{ property.antiquity }}</p>
                    <p><strong>Propietario:</strong> {{ property.owner }}</p>
                    <div class="property-images">
                        {% for image in property.images %}
                        <img src="{{ image }}" alt="Imagen de la propiedad">
                        {% endfor %}
                    </div>
                    <a href="/details/{{ property.id }}">Ver más</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <footer>
        <p>&copy; 2024 Bienes Raíces. Todos los derechos reservados.</p>
    </footer>
</body>
</html>

        """

        return render_template_string(html, properties=property_list)

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"


@app.route('/detalles/<property_id>')
def detalles(property_id):
    # Redirigir temporalmente a una página de detalles ficticia
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

