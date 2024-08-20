from flask import Flask, render_template,request,redirect, url_for, request, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = '12345'

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
            agent_collection = db_connection.get_collection('Agent')
            agent = agent_collection.find_one({'_id': property.get('agent_id')})

            image_urls = property.get('images', ['static/images/placeholder.jpg'])
            property_list.append({
                'name': property.get('name', 'Nombre de la Propiedad'),
                'price': property.get('price', '0'),
                'transaction_type': property.get('transaction_type', 'Tipo de Transacción'),
                'antiquity': property.get('antiquity', 'Antigüedad'),
                'owner': property.get('owner', 'Propietario'),
                'images': image_urls,
                'id': str(property.get('_id')),
                'agent_id': str(agent.get('id_user')) if agent else None
            })

        db_connection.close()

        return render_template('index.html', properties=property_list)

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"

    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db_connection = MongoDBConnection()
        users_collection = db_connection.get_collection('Users')
        roles_collection = db_connection.get_collection('Rol')

        user = users_collection.find_one({'email': email})

        if user and user.get('password') == password:
            role_id = user.get('role_id') 
            role = roles_collection.find_one({'_id': ObjectId(role_id)})  
            role_name = role.get('name') if role else 'Desconocido'
            
            session['user_id'] = str(user['_id'])
            session['user_role'] = role_name  
            
            db_connection.close()
            return redirect(url_for('index'))
        else:
            db_connection.close()
            return render_template('login.html', error='Credenciales incorrectas.')

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_role', None)
    return redirect(url_for('login'))



@app.route('/add_agent', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        db_connection = MongoDBConnection()
        users_collection = db_connection.get_collection('Users')
        roles_collection = db_connection.get_collection('Rol')
        agents_collection = db_connection.get_collection('Agent')
        
     
        role = roles_collection.find_one({"name": "Agente"})
        role_id = str(role['_id']) if role else None

        if not role_id:
            db_connection.close()
            return render_template('add_agent.html', error='Rol de Agente no encontrado.')

     
        new_user = {
            "password": request.form['password'],
            "birth_date": request.form['birth_date'],
            "first_sur_name": request.form['first_sur_name'],
            "second_sur_name": request.form['second_sur_name'],
            "name": request.form['name'],
            "identification": request.form['identification'],
            "email": request.form['email'],
            "phone": request.form['phone'],
            "image": request.form['image'],
            "role_id": ObjectId(role_id)  
        }
        
        user_id = users_collection.insert_one(new_user).inserted_id
        
        new_agent = {
            "id_user": ObjectId(user_id),
            "name": request.form['name'],
            "salary": request.form['salary'],  
            "experience": request.form['experience'],  
            "hire_date": datetime.now()  
        }
        
        agents_collection.insert_one(new_agent)

        db_connection.close()
        return redirect(url_for('view_agents'))

    return render_template('add_agent.html')

@app.route('/view_agents')
def view_agents():
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    users_collection = db_connection.get_collection('Users')

    agents = list(agents_collection.find())  

    for agent in agents:
        user = users_collection.find_one({"_id": ObjectId(agent['id_user'])})
        if user:
            agent['image'] = user.get('image', '')

        if isinstance(agent.get('hire_date'), datetime):
            agent['hire_date'] = agent['hire_date'].strftime('%d/%m/%Y')
        else:
            agent['hire_date'] = 'No disponible'

    db_connection.close()

    return render_template('view_agents.html', agents=agents)

@app.route('/view_interested')
def view_interested():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    
    user_id = session['user_id']
    
    try:
        db_connection = MongoDBConnection()
        contact_collection = db_connection.get_collection('Contact')
        property_collection = db_connection.get_collection('Property')
        agent_collection = db_connection.get_collection('Agent')

        agent = agent_collection.find_one({'id_user': ObjectId(user_id)})
        
        if not agent:
            db_connection.close()
            return "Agente no encontrado", 404

        agent_id = agent.get('_id')

        properties = list(property_collection.find({'agent_id': agent_id}))
        
        property_ids = [property.get('_id') for property in properties]
        contacts = list(contact_collection.find({'id_property': {'$in': property_ids}}))

        for contact in contacts:
            if isinstance(contact.get('date_contact'), datetime):
                contact['date_contact'] = contact['date_contact'].strftime('%d/%m/%Y')
            else:
                contact['date_contact'] = 'No disponible'
            contact['id_str'] = str(contact['_id'])

        db_connection.close()

        return render_template('view_interested.html', contacts=contacts)

    except Exception as e:
        db_connection.close()
        return f"Error en la operación de MongoDB: {e}"




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

            id_property = contact.get('id_property')
            if not id_property:
                return "El contacto no tiene una propiedad asociada."

            property_info = property_collection.find_one({'_id': ObjectId(id_property)})
            if not property_info:
                return "No se encontró la propiedad asociada."

            id_agent = property_info.get('agent_id')
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

    return render_template('schedule_appointment.html', contact=contact, available_dates=available_dates)

@app.route('/confirmed_appointments')
def confirmed_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))  
    
    user_id = session['user_id']
    
    try:
        db_connection = MongoDBConnection()
        appointment_collection = db_connection.get_collection('Appointments')
        property_collection = db_connection.get_collection('Property')
        agent_collection = db_connection.get_collection('Agent')

        agent = agent_collection.find_one({'id_user': ObjectId(user_id)})
        
        if not agent:
            db_connection.close()
            return "Agente no encontrado", 404

        agent_id = agent.get('_id')

        appointments = appointment_collection.find({'status': 'confirmada', 'agent_id': agent_id})

        appointments_details = []

        for appointment in appointments:
            property_info = property_collection.find_one({'_id': appointment['id_property']})

            appointment_detail = {
                'property_name': property_info['name'] if property_info else 'N/A',
                'contact_name': appointment.get('name', 'N/A'),
                'contact_phone': appointment.get('phone', 'N/A'),
                'contact_email': appointment.get('email', 'N/A'),
                'selected_date': appointment['selected_date'].strftime('%Y-%m-%d') if appointment.get('selected_date') else 'N/A',
                'status': appointment['status']
            }

            appointments_details.append(appointment_detail)

        db_connection.close()

        return render_template('confirmed_appointments.html', appointments=appointments_details)

    except Exception as e:
        db_connection.close()
        return f"Error en la operación de MongoDB: {e}"


@app.route('/delete_agent/<agent_id>')
def delete_agent(agent_id):
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    roles_collection = db_connection.get_collection('Rol')
    users_collection = db_connection.get_collection('Users')

    agent = agents_collection.find_one({"_id": ObjectId(agent_id)})
    
    if agent:
        agents_collection.delete_one({"_id": ObjectId(agent_id)})

        users_collection.delete_one({"_id": ObjectId(agent['id_user'])})

    db_connection.close()
    return redirect(url_for('view_agents'))


@app.route('/edit_agent/<agent_id>', methods=['GET', 'POST'])
def edit_agent(agent_id):
    db_connection = MongoDBConnection()
    agents_collection = db_connection.get_collection('Agent')
    users_collection = db_connection.get_collection('Users')

    if request.method == 'POST':
        updated_agent_data = {
            'salary': request.form['salary'],
            'experience': request.form['experience'],
            'hire_date': request.form['hire_date'], 
            'name': request.form['name']
        }
        agents_collection.update_one({"_id": ObjectId(agent_id)}, {"$set": updated_agent_data})

        user_id = request.form['user_id']
        updated_user_data = {
            'password': request.form['password'],
            'birth_date': request.form['birth_date'],  
            'name': request.form['user_name'],
            'identification': request.form.get('identification', ''),  
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

    return render_template('edit_agent.html', agent=agent, user=user)


@app.route('/properties')
def properties():
    db_connection = MongoDBConnection()
    properties_collection = db_connection.get_collection('Properties')
    properties = properties_collection.find()
    
    # Convertir el cursor a una lista de diccionarios
    properties_list = list(properties)
    
    db_connection.close()
    return render_template('properties.html', properties=properties_list)

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

        # Obtener URLs de las imágenes
        image_urls = request.form.getlist('image_url')  # Manejar múltiples URLs

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

        # Obtener el ID del usuario actual
        user_id = session.get('user_id')  # Asegúrate de que el user_id esté almacenado en la sesión

        # Guardar propiedad
        property_collection.insert_one({
            'name': name,
            'price': price,
            'transaction_type': transaction_type,
            'antiquity': antiquity,
            'owner': owner,
            'id_characteristics': characteristics_id,
            'id_address': address_id,
            'images': image_urls,  # Guardar URLs de imágenes directamente
            'agent_id': agent_id,  # Guardar agent_id como ObjectId
        })

        db_connection.close()
        return redirect(url_for('index'))  # Asegúrate de que 'index' sea una ruta válida

    # Obtener lista de agentes
    agents = list(agent_collection.find({}))

    return render_template('add_property.html', agents=agents)

@app.route('/edit_property/<property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    db_connection = MongoDBConnection()
    property_collection = db_connection.get_collection('Property')
    agent_collection = db_connection.get_collection('Agent')

    property = property_collection.find_one({'_id': ObjectId(property_id)})

    if not property:
        db_connection.close()
        return "Propiedad no encontrada", 404

    user_id = session['user_id']
    agent = agent_collection.find_one({'_id': property.get('agent_id')})

    if not agent:
        db_connection.close()
        return "Agente no encontrado", 404
    
    if agent.get('id_user') != ObjectId(user_id):
        db_connection.close()
        return "No tienes permiso para editar esta propiedad", 403

    if request.method == 'POST':
        try:
            images = request.form.getlist('existing_images')
            new_image_url = request.form.get('new_image')

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

    db_connection.close()
    return render_template('edit_property.html', property=property, property_id=property_id)


@app.route('/delete_property/<property_id>')
def delete_property(property_id):
    if 'user_id' not in session:
        return redirect(url_for('login')) 

    db_connection = MongoDBConnection()
    property_collection = db_connection.get_collection('Property')
    agent_collection = db_connection.get_collection('Agent')

    property = property_collection.find_one({'_id': ObjectId(property_id)})

    if not property:
        db_connection.close()
        return "Propiedad no encontrada", 404

    user_id = session['user_id']

    agent = agent_collection.find_one({'_id': property.get('agent_id')})
    
    if not agent:
        db_connection.close()
        return "Agente no encontrado", 404
    
    if agent.get('id_user') != ObjectId(user_id):
        db_connection.close()
        return "No tienes permiso para eliminar esta propiedad", 403

    try:
        property_collection.delete_one({'_id': ObjectId(property_id)})
        db_connection.close()
        return redirect(url_for('index'))

    except Exception as e:
        db_connection.close()
        return f"Error en la operación de MongoDB: {e}"

if __name__ == '__main__':
    app.run(debug=True)