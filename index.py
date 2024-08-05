from flask import Flask, render_template_string, redirect, url_for, request
from pymongo import MongoClient
from bson import ObjectId

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
                    position: relative;
                }
                .container {
                    width: 80%;
                    margin: 0 auto;
                    overflow: hidden;
                }
                .login-button {
                    position: absolute;
                    top: 50%;
                    right: 1rem;
                    transform: translateY(-50%);
                    background-color: #fff;
                    color: #007BFF;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .login-button:hover {
                    background-color: #f0f0f0;
                }
                .add-property-button {
                    position: absolute;
                    top: 50%;
                    right: 6rem;
                    transform: translateY(-50%);
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }
                .add-property-button:hover {
                    background-color: #0056b3;
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
                .buttons {
                    margin-top: 1rem;
                }
                .buttons button {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-right: 0.5rem;
                }
                .buttons button:hover {
                    background-color: #0056b3;
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
                    <a href="/login">
                        <button class="login-button">Iniciar Sesión</button>
                    </a>
                    <a href="/add_property" class="add-property-button">Agregar Propiedad</a>
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
                            <div class="buttons">
                              <a href="{{ url_for('details', property_id=property.id) }}"><button>Detalles</button></a>
                                <a href="{{ url_for('edit_property', property_id=property.id) }}"><button>Editar</button></a>
                                <a href="{{ url_for('delete_property', property_id=property.id) }}"><button>Eliminar</button></a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html, properties=property_list)

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        try:
            new_property = {
                'name': request.form.get('name'),
                'price': float(request.form.get('price')),
                'transaction_type': request.form.get('transaction_type'),
                'antiquity': int(request.form.get('antiquity')),
                'owner': request.form.get('owner'),
                'images': []  # Add logic for images if needed
            }

            db_connection = MongoDBConnection()
            property_collection = db_connection.get_collection('Property')
            property_collection.insert_one(new_property)
            db_connection.close()
            return redirect(url_for('index'))

        except Exception as e:
            return f"Error al agregar la propiedad: {e}"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agregar Propiedad</title>
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
            form {
                background: #fff;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
            }
            label {
                margin: 0.5rem 0;
            }
            input[type="text"],
            input[type="number"],
            input[type="submit"] {
                padding: 0.5rem;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 0.5rem 0;
                font-size: 1rem;
            }
            input[type="submit"] {
                background-color: #007BFF;
                color: #fff;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #0056b3;
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
                <h1>Agregar Nueva Propiedad</h1>
            </div>
        </header>
        <div class="container">
            <form action="/add_property" method="POST">
                <label for="name">Nombre:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="price">Precio:</label>
                <input type="number" id="price" name="price" step="0.01" required>
                
                <label for="transaction_type">Tipo de Transacción:</label>
                <input type="text" id="transaction_type" name="transaction_type" required>
                
                <label for="antiquity">Años de Antigüedad:</label>
                <input type="number" id="antiquity" name="antiquity" required>
                
                <label for="owner">Propietario:</label>
                <input type="text" id="owner" name="owner" required>
                
                <input type="submit" value="Agregar Propiedad">
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/edit_property/<property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    db_connection = MongoDBConnection()
    property_collection = db_connection.get_collection('Property')

    if request.method == 'POST':
        try:
            updated_property = {
                'name': request.form.get('name'),
                'price': float(request.form.get('price')),
                'transaction_type': request.form.get('transaction_type'),
                'antiquity': int(request.form.get('antiquity')),
                'owner': request.form.get('owner'),
                'images': []  # Update image URLs if needed
            }

            property_collection.update_one({'_id': ObjectId(property_id)}, {'$set': updated_property})
            db_connection.close()
            return redirect(url_for('index'))

        except Exception as e:
            db_connection.close()
            return f"Error en la operación de MongoDB: {e}"

    property = property_collection.find_one({'_id': ObjectId(property_id)})
    db_connection.close()

    if property:
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Editar Propiedad</title>
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
                form {
                    background: #fff;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    display: flex;
                    flex-direction: column;
                }
                label {
                    margin: 0.5rem 0;
                }
                input[type="text"],
                input[type="number"],
                input[type="submit"] {
                    padding: 0.5rem;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin: 0.5rem 0;
                    font-size: 1rem;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
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
                    <h1>Editar Propiedad</h1>
                </div>
            </header>
            <div class="container">
                <form action="{{ url_for('edit_property', property_id=property_id) }}" method="POST">
                    <label for="name">Nombre:</label>
                    <input type="text" id="name" name="name" value="{{ property['name'] }}" required>
                    
                    <label for="price">Precio:</label>
                    <input type="number" id="price" name="price" step="0.01" value="{{ property['price'] }}" required>
                    
                    <label for="transaction_type">Tipo de Transacción:</label>
                    <input type="text" id="transaction_type" name="transaction_type" value="{{ property['transaction_type'] }}" required>
                    
                    <label for="antiquity">Años de Antigüedad:</label>
                    <input type="number" id="antiquity" name="antiquity" value="{{ property['antiquity'] }}" required>
                    
                    <label for="owner">Propietario:</label>
                    <input type="text" id="owner" name="owner" value="{{ property['owner'] }}" required>
                    
                    <input type="submit" value="Guardar Cambios">
                </form>
            </div>
        </body>
        </html>
        """
        return render_template_string(html, property=property, property_id=property_id)
    else:
        return "Propiedad no encontrada", 404

@app.route('/delete_property/<property_id>')
def delete_property(property_id):
    try:
        db_connection = MongoDBConnection()
        property_collection = db_connection.get_collection('Property')

        property_collection.delete_one({'_id': ObjectId(property_id)})
        db_connection.close()
        return redirect(url_for('index'))

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"

if __name__ == '__main__':
    app.run(debug=True)
