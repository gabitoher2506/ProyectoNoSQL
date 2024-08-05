from flask import render_template_string, request, redirect, url_for
from bson import ObjectId
from app import app  # Asegúrate de importar app desde app.py
from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri='mongodb+srv://msolano80258:Francia9192@cluster0.6uxqadh.mongodb.net/?retryWrites=true&w=majority'):
        try:
            self.client = MongoClient(uri)
            self.db = self.client['ProyectoNosql']
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        first_sur_name = request.form.get('first_sur_name')
        second_sur_name = request.form.get('second_sur_name')
        email = request.form.get('email')
        password = request.form.get('password')
        birth_date = request.form.get('birth_date')
        identification = request.form.get('identification')
        phone = request.form.get('phone')
        image = request.form.get('image')

        # Insert into MongoDB
        db_connection = MongoDBConnection()
        users_collection = db_connection.get_collection('Users')
        roles_collection = db_connection.get_collection('Rol')

        # Create a new user
        user_id = users_collection.insert_one({
            'name': name,
            'first_sur_name': first_sur_name,
            'second_sur_name': second_sur_name,
            'email': email,
            'password': password,
            'birth_date': birth_date,
            'identification': identification,
            'phone': phone,
            'image': image
        }).inserted_id

        # Assign role to the new user
        roles_collection.insert_one({
            'name': 'Admin',
            'id_user': ObjectId(user_id)
        })

        db_connection.close()
        return redirect(url_for('login'))

    html = """
    <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(to right, #4a90e2, #50c2c9);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #333;
        }
        header {
            background-color: #007BFF;
            color: #fff;
            padding: 1.5rem 0;
            text-align: center;
            position: fixed;
            top: 0;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .header-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        .header-content h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: bold;
        }
        .header-content p {
            margin: 0;
            font-size: 1.2rem;
            color: #e1e1e1;
        }
        .container {
            width: 90%;
            max-width: 500px;
            padding: 2rem;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            position: relative;
            top: 70px;
            text-align: center;
        }
        .register-form {
            display: flex;
            flex-direction: column;
        }
        .register-form input {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            border: 1px solid #ddd;
            box-sizing: border-box;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s, box-shadow 0.3s;
            background-color: #f9f9f9;
        }
        .register-form input:focus {
            border-color: #007BFF;
            box-shadow: 0 0 8px rgba(0,123,255,0.5);
            background-color: #fff;
        }
        .register-form button {
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 8px;
            background-color: #007BFF;
            color: #fff;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
            font-weight: bold;
        }
        .register-form button:hover {
            background-color: #0056b3;
            transform: scale(1.02);
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
            <div class="header-content">
                <h1>Registro de Usuario</h1>
                <p>Complete el formulario para registrarse</p>
            </div>
        </header>
        <div class="container">
            <div class="register-form">
                <form method="POST">
                    <input type="text" name="name" placeholder="Nombre" required>
                    <input type="text" name="first_sur_name" placeholder="Primer Apellido" required>
                    <input type="text" name="second_sur_name" placeholder="Segundo Apellido">
                    <input type="email" name="email" placeholder="Correo Electrónico" required>
                    <input type="password" name="password" placeholder="Contraseña" required>
                    <input type="date" name="birth_date" placeholder="Fecha de Nacimiento" required>
                    <input type="text" name="identification" placeholder="Identificación" required>
                    <input type="text" name="phone" placeholder="Teléfono" required>
                    <input type="text" name="image" placeholder="Imagen (URL)">
                    <button type="submit">Registrar</button>
                </form>
            </div>
        </div>
        
    </body>
    </html>
    """
    return render_template_string(html)
