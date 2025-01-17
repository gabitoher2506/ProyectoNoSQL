from flask import Flask, render_template_string, abort, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

# Utilizar la instancia de app desde app.py
from app import app

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

@app.route('/details/<property_id>')
def details(property_id):
    try:
        db_connection = MongoDBConnection()
        property_collection = db_connection.get_collection('Property')
        characteristics_collection = db_connection.get_collection('Characteristics_Property')

        # Recuperar la propiedad usando el ID
        property = property_collection.find_one({'_id': ObjectId(property_id)})
        if not property:
            return "Propiedad no encontrada", 404

        # Recuperar las características usando el id_characteristics de la propiedad
        characteristics_id = property.get('id_characteristics')
        if characteristics_id:
            characteristics = characteristics_collection.find_one({'_id': ObjectId(characteristics_id)})
        else:
            characteristics = {}

        # Preparar los datos para la plantilla
        property_details = {
            'name': property.get('name', 'Nombre de la Propiedad'),
            'price': property.get('price', '0'),
            'transaction_type': property.get('transaction_type', 'Tipo de Transacción'),
            'antiquity': property.get('antiquity', '0'),
            'owner': property.get('owner', 'Propietario'),
            'images': property.get('images', ['static/images/placeholder.jpg']),
            'characteristics': characteristics or {}
        }

        db_connection.close()

        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Detalles de la Propiedad</title>
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
                .property-details {
                    background: #fff;
                    margin: 1rem 0;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .property-images {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                }
                .property-images img {
                    width: 300px;
                    height: 200px;
                    object-fit: cover;
                    border-radius: 8px;
                }
                .property-info h2 {
                    margin-top: 0;
                }
                .property-info p {
                    margin: 0.5rem 0;
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
                .contact-button {
                    display: block;
                    width: 100%;
                    padding: 1rem;
                    font-size: 1rem;
                    color: #fff;
                    background-color: #007BFF;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 1rem;
                }
                .contact-button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Detalles de la Propiedad</h1>
                </div>
            </header>
            <div class="container">
                <div class="property-details">
                    <h2>{{ property.name }}</h2>
                    <p><strong>Precio:</strong> ${{ property.price }}</p>
                    <p><strong>Tipo de Transacción:</strong> {{ property.transaction_type }}</p
                    <p><strong>Años de Antigüedad:</strong> {{ property.antiquity }}</p>
                    <p><strong>Propietario:</strong> {{ property.owner }}</p>
                    <div class="property-images">
                        {% for image in property.images %}
                        <img src="{{ image }}" alt="Imagen de la propiedad">
                        {% endfor %}
                    </div>
                    <div class="property-characteristics">
                        <h3>Características</h3>
                        <ul>
                            <li><strong>Número de Habitaciones:</strong> {{ property.characteristics.number_rooms }}</li>
                            <li><strong>Número de Baños:</strong> {{ property.characteristics.number_bathrooms }}</li>
                            <li><strong>Descripción:</strong> {{ property.characteristics.description }}</li>
                            <li><strong>Garage:</strong> {{ property.characteristics.garage }}</li>
                            <li><strong>Pool:</strong> {{ property.characteristics.pool }}</li>
                        </ul>
                    </div>
                    <a href="{{ url_for('contacto', property_id=property_id) }}" class="contact-button">Contactar Vendedor</a>
                </div>
            </div>
            
        </body>
        </html>
        """

        return render_template_string(html, property=property_details, property_id=property_id)

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"
