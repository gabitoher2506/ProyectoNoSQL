from flask import Flask, render_template_string, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

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

@app.route('/contacto/<property_id>', methods=['GET', 'POST'])
def contacto(property_id):
    if request.method == 'POST':
        try:
            db_connection = MongoDBConnection()
            contact_collection = db_connection.get_collection('Contact')

            contact_data = {
                'id_property': ObjectId(property_id),
                'date_contact': datetime.now(),
                'name': request.form['name'],
                'phone': request.form['phone'],
                'email': request.form['email'],
                'message': request.form['message']
            }

            contact_collection.insert_one(contact_data)
            db_connection.close()

            return redirect(url_for('details', property_id=property_id))
        except Exception as e:
            return f"Error en la operación de MongoDB: {e}"
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contactar Vendedor</title>
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
            .contact-form {
                background: #fff;
                margin: 1rem 0;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .contact-form h2 {
                margin-top: 0;
            }
            .contact-form input, .contact-form textarea {
                width: 100%;
                padding: 10px;
                margin: 5px 0 10px 0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .contact-form button {
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
            .contact-form button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <h1>Contactar Vendedor</h1>
            </div>
        </header>
        <div class="container">
            <div class="contact-form">
                <h2>Envíe sus datos</h2>
                <form method="POST">
                    <input type="text" name="name" placeholder="Nombre" required>
                    <input type="tel" name="phone" placeholder="Teléfono" required>
                    <input type="email" name="email" placeholder="Correo Electrónico" required>
                    <textarea name="message" placeholder="Mensaje" required></textarea>
                    <button type="submit">Enviar</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)
