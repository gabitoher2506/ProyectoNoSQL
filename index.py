from flask import Flask, render_template_string, redirect, url_for, request
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime 

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
        
        .add-agent-button"{
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
        
        .add-agent-button:hover {
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
            <a href="/add_agent" class="add-property-button">Agregar Agente</a>
            <a href="/view_agents" class="add-property-button">Agente</a>
            <a href="/view_interested" class="add-property-button">Interesados</a>
            <a href="/confirmed_appointments" class="add-property-button">Citas Confirmadas</a>
          

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
    
    
    
@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        db_connection = MongoDBConnection()
        users_collection = db_connection.get_collection('Users')
        roles_collection = db_connection.get_collection('Rol')
        agents_collection = db_connection.get_collection('Agent')
        
        # Crear nuevo usuario
        new_user = {
            "password": request.form['password'],
            "birth_date": request.form['birth_date'],
            "first_sur_name": request.form['first_sur_name'],
            "second_sur_name": request.form['second_sur_name'],
            "name": request.form['name'],
            "identification": request.form['identification'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "image": request.form['image']
        }
        
        # Insertar el nuevo usuario en la colección Users
        user_id = users_collection.insert_one(new_user).inserted_id
        
        # Asignar rol de "Agente" al nuevo usuario
        new_role = {
            "name": "Agente",
            "id_user": str(user_id)
        }
        
        # Insertar el rol en la colección Rol
        roles_collection.insert_one(new_role)

        # Crear un nuevo documento en la colección Agent
        new_agent = {
            "id_user": str(user_id),
            "name": request.form['name'],
            "salary": request.form['salary'],  # Suponiendo que se captura el salario en el formulario
            "experience": request.form['experience'],  # Suponiendo que se captura la experiencia en el formulario
            "hire_date": datetime.now()  # Fecha de contratación actual
        }
        
        # Insertar el nuevo agente en la colección Agent
        agents_collection.insert_one(new_agent)

        db_connection.close()
        return redirect(url_for('view_agents'))

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            
            <title>Agregar Agente</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                .form-container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .form-group {
                    margin-bottom: 15px;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                }
                .form-group input {
                    width: 100%;
                    padding: 8px;
                    box-sizing: border-box;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                .form-group button {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                .form-group button:hover {
                    background-color: #0056b3;
                }
                
                 
                .back-button {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background-color: #6c757d;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 16px;
                }
                .back-button:hover {
                    background-color: #5a6268;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>Agregar Nuevo Agente</h2>
                <a href="{{ url_for('index') }}" class="back-button">Menú</a>
                <form method="post">
                    <div class="form-group">
                        <label for="name">Nombre:</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="first_sur_name">Primer Apellido:</label>
                        <input type="text" id="first_sur_name" name="first_sur_name" required>
                    </div>
                    <div class="form-group">
                        <label for="second_sur_name">Segundo Apellido:</label>
                        <input type="text" id="second_sur_name" name="second_sur_name" required>
                    </div>
                    <div class="form-group">
                        <label for="identification">Identificación:</label>
                        <input type="text" id="identification" name="identification" required>
                    </div>
                    <div class="form-group">
                        <label for="birth_date">Fecha de Nacimiento:</label>
                        <input type="date" id="birth_date" name="birth_date" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Correo Electrónico:</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="phone">Teléfono:</label>
                        <input type="text" id="phone" name="phone" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Contraseña:</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <div class="form-group">
                        <label for="image">URL de la Imagen:</label>
                        <input type="text" id="image" name="image">
                    </div>
                    <div class="form-group">
                        <label for="salary">Salario:</label>
                        <input type="text" id="salary" name="salary" required>
                    </div>
                    <div class="form-group">
                        <label for="experience">Experiencia:</label>
                        <input type="text" id="experience" name="experience" required>
                    </div>
                    <div class="form-group">
                        <button type="submit">Agregar Agente</button>
                    </div>
                </form>
            </div>
            
        </body>
        </html>
    ''')

@app.route('/view_agents')
def view_agents():
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    users_collection = db_connection.get_collection('Users')

    agents = list(agents_collection.find())  # Obtener todos los agentes de la colección

    # Combinar información de la colección de agentes con la colección de usuarios para obtener la imagen
    for agent in agents:
        user = users_collection.find_one({"_id": ObjectId(agent['id_user'])})
        if user:
            agent['image'] = user.get('image', '')

        # Convertir la fecha de contratación a cadena en formato 'dd/mm/yyyy'
        if isinstance(agent.get('hire_date'), str):
            try:
                agent['hire_date'] = datetime.fromisoformat(agent['hire_date']).strftime('%d/%m/%Y')
            except ValueError:
                agent['hire_date'] = 'No disponible'

    db_connection.close()

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de Agentes</title>
            
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                .agents-container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .agent {
                    margin-bottom: 15px;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background-color: #fafafa;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                .agent img {
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    margin-right: 20px;
                }
                .agent h3 {
                    margin: 0;
                }
                .agent p {
                    margin: 5px 0;
                }
                
                .edit-button, .delete-button {
                    display: inline-block;
                    margin-left: 10px;
                    padding: 5px 10px;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 14px;
                }
                .edit-button {
                    background-color: #007bff;
                }
                .edit-button:hover {
                    background-color: #0056b3;
                }
                .delete-button {
                    background-color: #dc3545;
                }
                .delete-button:hover {
                    background-color: #c82333;
                }
                .back-button {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background-color: #6c757d;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 16px;
                }
                .back-button:hover {
                    background-color: #5a6268;
                }
            </style>
        </head>
        <body>
            <div class="agents-container">
                <h2>Lista de Agentes Registrados</h2>
                <a href="{{ url_for('index') }}" class="back-button">Menú</a>
                {% for agent in agents %}
                <div class="agent">
                    <img src="{{ agent.image }}" alt="Imagen de {{ agent.name }}">
                    <div>
                        <h3>{{ agent.name }}</h3>
                        <p><strong>Salario:</strong> {{ agent.salary }}</p>
                        <p><strong>Experiencia:</strong> {{ agent.experience }}</p>
                        <p><strong>Fecha de Contratación:</strong> {{ agent.hire_date }}</p>
                    </div>
                    <div>
                        <a href="{{ url_for('edit_agent', agent_id=agent._id) }}" class="edit-button">Editar</a>
                        <a href="{{ url_for('delete_agent', agent_id=agent._id) }}" class="delete-button" onclick="return confirm('¿Estás seguro de que quieres eliminar este agente?')">Eliminar</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', agents=agents)
@app.route('/view_interested')
def view_interested():
    db_connection = MongoDBConnection()
    contact_collection = db_connection.get_collection('Contact')

    contacts = list(contact_collection.find())  # Obtener todos los contactos de la colección

    # Convertir la fecha de contacto a cadena en formato 'dd/mm/yyyy'
    for contact in contacts:
        if isinstance(contact.get('date_contact'), str):
            try:
                contact['date_contact'] = datetime.fromisoformat(contact['date_contact']).strftime('%d/%m/%Y')
            except ValueError:
                contact['date_contact'] = 'No disponible'
        else:
            contact['date_contact'] = 'No disponible'
        # Convertir _id a cadena para usar en la plantilla
        contact['id_str'] = str(contact['_id'])

    db_connection.close()

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lista de Interesados</title>
            <style>
                body {
                    font-family: 'Roboto', sans-serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 900px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #ffffff;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                    border-radius: 10px;
                }
                .container h2 {
                    margin-bottom: 30px;
                    font-size: 28px;
                    color: #333;
                    text-align: center;
                    border-bottom: 2px solid #007bff;
                    padding-bottom: 10px;
                }
                .contact-card {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    background-color: #f7f9fc;
                    margin-bottom: 20px;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    transition: transform 0.2s ease;
                }
                .contact-card:hover {
                    transform: translateY(-5px);
                }
                .contact-details {
                    max-width: 75%;
                }
                .contact-details h3 {
                    margin-top: 0;
                    font-size: 22px;
                    color: #007bff;
                }
                .contact-details p {
                    margin: 5px 0;
                    font-size: 16px;
                    color: #555;
                }
                .contact-details p strong {
                    color: #333;
                }
                .back-button {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 16px;
                    transition: background-color 0.3s ease;
                }
                .back-button:hover {
                    background-color: #0056b3;
                }
                .contact-icon {
                    font-size: 24px;
                    color: #007bff;
                    margin-right: 15px;
                }
                .contact-details p .contact-icon {
                    font-size: 18px;
                }
                .schedule-button {
                    display: inline-block;
                    margin-top: 10px;
                    padding: 10px 20px;
                    background-color: #28a745;
                    color: #fff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    text-decoration: none;
                    font-size: 16px;
                    transition: background-color 0.3s ease;
                }
                .schedule-button:hover {
                    background-color: #218838;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Lista de Interesados</h2>
                <a href="{{ url_for('index') }}" class="back-button">Menú</a>
                {% for contact in contacts %}
                <div class="contact-card">
                    <div class="contact-details">
                        <h3>{{ contact.name }}</h3>
                        <p><strong><span class="contact-icon">📞</span>Teléfono:</strong> {{ contact.phone }}</p>
                        <p><strong><span class="contact-icon">📧</span>Email:</strong> {{ contact.email }}</p>
                        <p><strong><span class="contact-icon">💬</span>Mensaje:</strong> {{ contact.message }}</p>
                        <p><strong><span class="contact-icon">📅</span>Fecha de Contacto:</strong> {{ contact.date_contact }}</p>
                        <p><strong><span class="contact-icon">📅</span>Fechas Disponibles:</strong>
                        {% if contact.available_dates %}
                            <ul>
                                {% for date in contact.available_dates %}
                                    <li>{{ date }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            No disponible
                        {% endif %}
                        </p>
                        <a href="{{ url_for('schedule_appointment', contact_id=contact.id_str) }}" class="schedule-button">Programar Cita</a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', contacts=contacts)

@app.route('/schedule/<contact_id>', methods=['GET', 'POST'])
def schedule_appointment(contact_id):
    db_connection = MongoDBConnection()
    contact_collection = db_connection.get_collection('Contact')
    appointment_collection = db_connection.get_collection('Appointments')
    property_collection = db_connection.get_collection('Property')

    contact = contact_collection.find_one({'_id': ObjectId(contact_id)})

    if request.method == 'POST':
        try:
            selected_date = request.form['selected_date']

            # Obtener `id_property` del contacto
            id_property = contact.get('id_property')
            if not id_property:
                return "El contacto no tiene una propiedad asociada."

            # Obtener `id_agent` usando `id_property`
            property_info = property_collection.find_one({'_id': ObjectId(id_property)})
            if not property_info:
                return "No se encontró la propiedad asociada."

            id_agent = property_info.get('id_agent')
            if not id_agent:
                return "No se encontró un agente asociado a la propiedad."

            appointment_data = {
                'id_contact': ObjectId(contact_id),
                'id_property': ObjectId(id_property),
                'date_contact': datetime.now(),
                'name': contact['name'],
                'phone': contact['phone'],
                'email': contact['email'],
                'available_dates': contact.get('available_dates', []),
                'selected_date': datetime.strptime(selected_date, '%Y-%m-%d'),
                'agent_id': ObjectId(id_agent),
                'status': 'confirmada'
            }

            appointment_collection.insert_one(appointment_data)
            db_connection.close()

            return redirect(url_for('view_interested'))
        except Exception as e:
            return f"Error en la operación de MongoDB: {e}"
    
    available_dates = contact.get('available_dates', [])

    db_connection.close()

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Programar Cita</title>
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
                .schedule-form {
                    background: #fff;
                    margin: 1rem 0;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .schedule-form h2 {
                    margin-top: 0;
                }
                .schedule-form input, .schedule-form select {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                .schedule-form button {
                    display: block;
                    width: 100%;
                    padding: 1rem;
                    font-size: 1rem;
                    color: #fff;
                    background-color: #007BFF;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .schedule-form button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Programar Cita</h1>
                </div>
            </header>
            <div class="container">
                <div class="schedule-form">
                    <h2>Seleccione una Fecha</h2>
                    <form method="POST">
                        <label for="selected_date">Fecha:</label>
                        <select name="selected_date" id="selected_date" required>
                            {% for date in available_dates %}
                                <option value="{{ date }}">{{ date }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit">Confirmar Cita</button>
                    </form>
                </div>
            </div>
        </body>
        </html>
    ''', contact=contact, available_dates=available_dates)
@app.route('/confirmed_appointments')
def confirmed_appointments():
    db_connection = MongoDBConnection()
    appointment_collection = db_connection.get_collection('Appointments')
    property_collection = db_connection.get_collection('Property')
    agent_collection = db_connection.get_collection('Agent')

    # Obtener todas las citas confirmadas
    appointments = appointment_collection.find({'status': 'confirmada'})

    # Lista para almacenar los detalles de cada cita
    appointments_details = []

    for appointment in appointments:
        # Obtener detalles de la propiedad
        property_info = property_collection.find_one({'_id': appointment['id_property']})

        # Obtener detalles del agente
        agent_info = agent_collection.find_one({'_id': appointment['agent_id']})

        # Construir el diccionario con los detalles de la cita
        appointment_detail = {
            'property_name': property_info['name'] if property_info else 'N/A',
            'agent_name': agent_info['name'] if agent_info else 'N/A',
            'contact_name': appointment.get('name', 'N/A'),
            'contact_phone': appointment.get('phone', 'N/A'),
            'contact_email': appointment.get('email', 'N/A'),
            'selected_date': appointment['selected_date'].strftime('%Y-%m-%d') if appointment.get('selected_date') else 'N/A',
            'status': appointment['status']
        }

        appointments_details.append(appointment_detail)

    db_connection.close()

    # Renderizar la plantilla con los detalles de las citas
    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Citas Confirmadas</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
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
                    padding: 1rem;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                }
                table, th, td {
                    border: 1px solid #ccc;
                }
                th, td {
                    padding: 0.75rem;
                    text-align: left;
                }
                th {
                    background-color: #007BFF;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <h1>Citas Confirmadas</h1>
                </div>
            </header>
            <div class="container">
                <table>
                    <thead>
                        <tr>
                            <th>Nombre de la Propiedad</th>
                            <th>Nombre del Agente</th>
                            <th>Nombre del Contacto</th>
                            <th>Teléfono del Contacto</th>
                            <th>Email del Contacto</th>
                            <th>Fecha Elegida</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for appointment in appointments %}
                        <tr>
                            <td>{{ appointment.property_name }}</td>
                            <td>{{ appointment.agent_name }}</td>
                            <td>{{ appointment.contact_name }}</td>
                            <td>{{ appointment.contact_phone }}</td>
                            <td>{{ appointment.contact_email }}</td>
                            <td>{{ appointment.selected_date }}</td>
                            <td>{{ appointment.status }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    ''', appointments=appointments_details)




@app.route('/delete_agent/<agent_id>')
def delete_agent(agent_id):
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    roles_collection = db_connection.get_collection('Rol')
    users_collection = db_connection.get_collection('Users')

    agent = agents_collection.find_one({"_id": ObjectId(agent_id)})
    
    if agent:
        # Eliminar el agente
        agents_collection.delete_one({"_id": ObjectId(agent_id)})

        # Eliminar el rol relacionado
        roles_collection.delete_many({"id_user": agent['id_user']})

        # Eliminar el usuario relacionado
        users_collection.delete_one({"_id": ObjectId(agent['id_user'])})

    db_connection.close()

    return redirect(url_for('view_agents'))

@app.route('/edit_agent/<agent_id>', methods=['GET', 'POST'])
def edit_agent(agent_id):
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    users_collection = db_connection.get_collection('Users')

    if request.method == 'POST':
        # Actualizar los datos del agente
        updated_agent_data = {
            'salary': request.form['salary'],
            'experience': request.form['experience'],
            'hire_date': request.form['hire_date'],  # Se guarda como str
            'name': request.form['name']
        }
        agents_collection.update_one({"_id": ObjectId(agent_id)}, {"$set": updated_agent_data})

        # Actualizar los datos del usuario asociado
        user_id = request.form['user_id']
        updated_user_data = {
            'password': request.form['password'],
            'birth_date': request.form['birth_date'],  # Se guarda como str
            'name': request.form['user_name'],
            'identification': request.form.get('identification', ''),  # Se usa .get para evitar KeyError
            'email': request.form['email'],
            'phone': request.form['phone'],
            'image': request.form['image']
        }
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user_data})

        db_connection.close()
        return redirect(url_for('view_agents'))

    # Obtener los detalles del agente y del usuario asociado
    agent = agents_collection.find_one({"_id": ObjectId(agent_id)})
    user = users_collection.find_one({"_id": ObjectId(agent['id_user'])})
    db_connection.close()

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Editar Agente</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }

                .container {
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 20px;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }

                h2 {
                    color: #333;
                    margin-bottom: 20px;
                    text-align: center;
                }

                form {
                    display: flex;
                    flex-direction: column;
                }

                .form-group {
                    margin-bottom: 15px;
                }

                .form-group label {
                    display: block;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #555;
                }

                .form-group input[type="text"],
                .form-group input[type="email"],
                .form-group input[type="password"],
                .form-group input[type="date"] {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }

                .form-group input[type="submit"] {
                    background-color: #28a745;
                    color: #fff;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background-color 0.3s;
                }

                .form-group input[type="submit"]:hover {
                    background-color: #218838;
                }

                input[type="hidden"] {
                    display: none;
                }

                a {
                    text-decoration: none;
                    color: #007bff;
                }

                a:hover {
                    text-decoration: underline;
                }

                /* Estilos para el botón de actualización */
                .form-group input[type="submit"] {
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 18px;
                    font-weight: bold;
                    text-transform: uppercase;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    transition: all 0.3s ease;
                    margin-top: 20px;
                }

                .form-group input[type="submit"]:hover {
                    background-color: #0056b3;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                    transform: translateY(-2px);
                }

                .form-group input[type="submit"]:active {
                    background-color: #004085;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    transform: translateY(0);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Editar Agente</h2>
                <form action="{{ url_for('edit_agent', agent_id=agent._id) }}" method="post">
                    <div class="form-group">
                        <label for="name">Nombre:</label>
                        <input type="text" id="name" name="name" value="{{ agent.name }}" required>
                    </div>
                    <div class="form-group">
                        <label for="salary">Salario:</label>
                        <input type="text" id="salary" name="salary" value="{{ agent.salary }}" required>
                    </div>
                    <div class="form-group">
                        <label for="experience">Experiencia:</label>
                        <input type="text" id="experience" name="experience" value="{{ agent.experience }}" required>
                    </div>
                    <div class="form-group">
                        <label for="hire_date">Fecha de Contratación:</label>
                        <input type="text" id="hire_date" name="hire_date" value="{{ agent.hire_date }}" required>
                    </div>
                    <input type="hidden" name="user_id" value="{{ user._id }}">
                    <div class="form-group">
                        <label for="user_name">Nombre de Usuario:</label>
                        <input type="text" id="user_name" name="user_name" value="{{ user.name }}" required>
                    </div>
                    <div class="form-group">
                        <label for="identification">Identificación:</label>
                        <input type="text" id="identification" name="identification" value="{{ user.identification }}" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Correo Electrónico:</label>
                        <input type="email" id="email" name="email" value="{{ user.email }}" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Contraseña:</label>
                        <input type="text" id="password" name="password" value="{{ user.password }}" required>
                    </div>
                    <div class="form-group">
                        <label for="birth_date">Fecha de Nacimiento:</label>
                        <input type="text" id="birth_date" name="birth_date" value="{{ user.birth_date }}" required>
                    </div>
                    <div class="form-group">
                        <label for="phone">Teléfono:</label>
                        <input type="text" id="phone" name="phone" value="{{ user.phone }}" required>
                    </div>
                    <div class="form-group">
                        <label for="image">Imagen:</label>
                        <input type="text" id="image" name="image" value="{{ user.image }}" required>
                    </div>
                    <div class="form-group">
                        <input type="submit" value="Actualizar">
                    </div>
                </form>
            </div>
        </body>
        </html>
    ''', agent=agent, user=user)


if __name__ == '__main__':
    app.run(debug=True)

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
