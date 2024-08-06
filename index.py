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
            display: inline-block;
            background-color: #007BFF;
            color: #fff;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            margin-top: 1rem;
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
            <a href="/add_property" class="add-property-button">Agregar Propiedad</a>
            <a href="/add_agent" class="add-agent-button">Agregar Agente</a>
            <a href="/login">
                <button class="login-button">Iniciar Sesión</button>
            </a>
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
    db_connection = MongoDBConnection()
    property_collection = db_connection.get_collection('Property')
    characteristics_collection = db_connection.get_collection('Characteristics_Property')
    address_collection = db_connection.get_collection('Address')
    agent_collection = db_connection.get_collection('Agent')

    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form.get('name')
        price = request.form.get('price')
        transaction_type = request.form.get('transaction_type')
        antiquity = request.form.get('antiquity')
        owner = request.form.get('owner')
        agent_id = request.form.get('agent_id')

        # Convertir agent_id a ObjectId
        agent_id = ObjectId(agent_id)

        # Obtener características
        number_rooms = request.form.get('number_rooms')
        number_bathrooms = request.form.get('number_bathrooms')
        description = request.form.get('description')
        garage = request.form.get('garage')
        pool = request.form.get('pool')

        # Obtener dirección
        street = request.form.get('street')
        province = request.form.get('province')
        canton = request.form.get('canton')
        others_signs = request.form.get('others_signs')

        # Obtener URL de la imagen
        image_urls = request.form.getlist('image_url')  # Para manejar múltiples URLs
        image_data = []
        for image_url in image_urls:
            if image_url:
                try:
                    # Descargar la imagen desde la URL
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_data.append(response.content)
                    else:
                        # Manejar el caso en que la imagen no se pueda descargar
                        print(f"Error al descargar la imagen: {image_url}")
                except Exception as e:
                    print(f"Error al descargar la imagen: {e}")

        # Guardar dirección
        address_id = address_collection.insert_one({
            'street': street,
            'province': province,
            'canton': canton,
            'others_signs': others_signs
        }).inserted_id

        # Guardar características
        characteristics_id = characteristics_collection.insert_one({
            'number_rooms': number_rooms,
            'number_bathrooms': number_bathrooms,
            'description': description,
            'garage': garage,
            'pool': pool
        }).inserted_id

        # Guardar propiedad
        property_collection.insert_one({
            'name': name,
            'price': price,
            'transaction_type': transaction_type,
            'antiquity': antiquity,
            'owner': owner,
            'id_characteristics': characteristics_id,
            'id_address': address_id,
            'images': image_urls,  # Guardar imágenes como array de binarios
            'agent_id': agent_id  # Guardar agent_id como ObjectId
        })

        db_connection.close()
        return redirect(url_for('index'))  # Asegúrate de que 'index' sea una ruta válida

    # Obtener lista de agentes
    agents = list(agent_collection.find({}))

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
                background-color: #333;
                color: #fff;
                padding: 10px 0;
                text-align: center;
            }
            main {
                padding: 20px;
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                margin-bottom: 20px;
                font-size: 24px;
            }
            label {
                display: block;
                margin: 10px 0 5px;
                font-size: 14px;
            }
            input[type="text"],
            input[type="number"],
            textarea,
            select {
                width: 100%;
                padding: 6px;
                margin-bottom: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            textarea {
                resize: vertical;
            }
            button {
                background-color: #333;
                color: #fff;
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover {
                background-color: #555;
            }
            h3 {
                margin-top: 20px;
                margin-bottom: 10px;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Agregar Nueva Propiedad</h1>
        </header>
        <main>
            <form method="POST">
                <label for="name">Nombre de la Propiedad:</label>
                <input type="text" id="name" name="name" required>

                <label for="price">Precio:</label>
                <input type="text" id="price" name="price" required>

                <label for="transaction_type">Tipo de Transacción:</label>
                <input type="text" id="transaction_type" name="transaction_type" required>

                <label for="antiquity">Años de Antigüedad:</label>
                <input type="text" id="antiquity" name="antiquity" required>

                <label for="owner">Propietario:</label>
                <input type="text" id="owner" name="owner" required>
                
                <h3>Agente</h3>
                <label for="agent_id">Seleccionar Agente:</label>
                <select id="agent_id" name="agent_id" required>
                    {% for agent in agents %}
                    <option value="{{ agent['_id'] }}">{{ agent['name'] }}</option>
                    {% endfor %}
                </select>

                <h3>Características</h3>
                <label for="number_rooms">Número de Habitaciones:</label>
                <input type="number" id="number_rooms" name="number_rooms" required>

                <label for="number_bathrooms">Número de Baños:</label>
                <input type="number" id="number_bathrooms" name="number_bathrooms" required>

                <label for="description">Descripción:</label>
                <textarea id="description" name="description" rows="3" required></textarea>

                <label for="garage">¿Tiene Garage?</label>
                <select id="garage" name="garage" required>
                    <option value="Sí">Sí</option>
                    <option value="No">No</option>
                </select>

                <label for="pool">¿Tiene Piscina?</label>
                <select id="pool" name="pool" required>
                    <option value="Sí">Sí</option>
                    <option value="No">No</option>
                </select>

                <h3>Dirección</h3>
                <label for="street">Calle:</label>
                <input type="text" id="street" name="street" required>

                <label for="province">Provincia:</label>
                <input type="text" id="province" name="province" required>

                <label for="canton">Cantón:</label>
                <input type="text" id="canton" name="canton" required>

                <label for="others_signs">Otros Señales:</label>
                <input type="text" id="others_signs" name="others_signs">

                <h3>Imágenes</h3>
                <label for="image_url">URL de Imagen (puedes agregar varias):</label>
                <input type="text" id="image_url" name="image_url" placeholder="https://ejemplo.com/imagen.jpg">

                <button type="submit">Agregar Propiedad</button>
            </form>
        </main>
    </body>
    </html>
    """
    return render_template_string(html, agents=agents)

@app.route('/edit_property/<property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    db_connection = MongoDBConnection()
    property_collection = db_connection.get_collection('Property')

    if request.method == 'POST':
        try:
            # Obtener las imágenes actuales y nuevas imágenes
            images = request.form.getlist('existing_images')
            new_image_url = request.form.get('new_image')

            # Agregar la nueva imagen si se proporcionó una URL
            if new_image_url:
                images.append(new_image_url)

            updated_property = {
                'name': request.form.get('name'),
                'price': float(request.form.get('price')),
                'transaction_type': request.form.get('transaction_type'),
                'antiquity': int(request.form.get('antiquity')),
                'owner': request.form.get('owner'),
                'images': images
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
                input[type="file"],
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
                .property-images .remove-image {
                    background: #ff0000;
                    color: #fff;
                    border: none;
                    padding: 0.3rem 0.5rem;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-left: 10px;
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
                <form action="{{ url_for('edit_property', property_id=property_id) }}" method="POST" enctype="multipart/form-data">
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

                    <label>Imágenes actuales:</label>
                    <div class="property-images">
                        {% for image in property['images'] %}
                        <div>
                            <img src="{{ image }}" alt="Imagen de la propiedad">
                            <button type="button" class="remove-image" onclick="removeImage('{{ image }}')">Eliminar</button>
                            <input type="hidden" name="existing_images" value="{{ image }}">
                        </div>
                        {% endfor %}
                    </div>

                    <label for="new_image">Nueva Imagen (URL):</label>
                    <input type="text" id="new_image" name="new_image">

                    <input type="submit" value="Guardar Cambios">
                </form>
            </div>
            <script>
                function removeImage(imageUrl) {
                    const inputs = document.querySelectorAll(`input[value='${imageUrl}']`);
                    inputs.forEach(input => input.remove());
                    const images = document.querySelectorAll(`img[src='${imageUrl}']`);
                    images.forEach(image => image.remove());
                    const buttons = document.querySelectorAll(`button[onclick="removeImage('${imageUrl}')"]`);
                    buttons.forEach(button => button.remove());
                }
            </script>
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
