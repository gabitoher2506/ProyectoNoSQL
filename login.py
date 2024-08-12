from flask import render_template_string, request, redirect, url_for, make_response
from werkzeug.security import check_password_hash
from app import app
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db_connection = MongoDBConnection()
        users_collection = db_connection.get_collection('Users')
        user = users_collection.find_one({'email': email})

        if user and check_password_hash(user.get('password'), password):
            db_connection.close()
            return redirect(url_for('index'))  # Asegúrate de que 'index' sea una ruta válida
        else:
            db_connection.close()
            html = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Iniciar Sesión</title>
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
                        position: absolute;
                        top: 0;
                        width: 100%;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }
                    .header-content {
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 0 1rem;
                    }
                    .header-content h1 {
                        margin: 0;
                        font-size: 2rem;
                    }
                    .header-content p {
                        margin: 0;
                        font-size: 1rem;
                        color: #e1e1e1;
                    }
                    .login-form {
                        display: flex;
                        flex-direction: column;
                        width: 90%;
                        max-width: 400px;
                        padding: 2rem;
                        background: #fff;
                        border-radius: 12px;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                        text-align: center;
                        margin-top: 80px;
                    }
                    .login-form input {
                        width: 100%;
                        padding: 0.75rem;
                        margin-bottom: 1rem;
                        border-radius: 8px;
                        border: 1px solid #ddd;
                        box-sizing: border-box;
                        font-size: 16px;
                        outline: none;
                        transition: border-color 0.3s, box-shadow 0.3s;
                    }
                    .login-form input:focus {
                        border-color: #007BFF;
                        box-shadow: 0 0 8px rgba(0,123,255,0.5);
                    }
                    .login-form button {
                        width: 100%;
                        padding: 0.75rem;
                        border: none;
                        border-radius: 8px;
                        background-color: #007BFF;
                        color: #fff;
                        font-size: 18px;
                        cursor: pointer;
                        transition: background-color 0.3s, transform 0.2s;
                    }
                    .login-form button:hover {
                        background-color: #0056b3;
                        transform: scale(1.02);
                    }
                    .register-button {
                        margin-top: 1rem;
                        padding: 0.75rem;
                        border: none;
                        border-radius: 8px;
                        background-color: #28a745;
                        color: #fff;
                        font-size: 16px;
                        cursor: pointer;
                        text-decoration: none;
                        display: inline-block;
                        transition: background-color 0.3s, transform 0.2s;
                    }
                    .register-button:hover {
                        background-color: #218838;
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
                        <h1>Bienvenido a Bienes Raíces</h1>
                        <p>Inicie sesión para continuar</p>
                    </div>
                </header>
                <div class="login-form">
                    <form method="POST">
                        <input type="email" name="email" placeholder="Correo Electrónico" required>
                        <input type="password" name="password" placeholder="Contraseña" required>
                        <button type="submit">Iniciar Sesión</button>
                    </form>
                    <a href="/register" class="register-button">Registrarse</a>
                    <p>Credenciales incorrectas. <a href="/login">Volver</a></p>
                </div>
                <footer>
                    <p>&copy; 2024 Bienes Raíces</p>
                </footer>
            </body>
            </html>
            """
            response = make_response(render_template_string(html))
            response.status_code = 401
            return response

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Iniciar Sesión</title>
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
                position: absolute;
                top: 0;
                width: 100%;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .header-content {
                max-width: 800px;
                margin: 0 auto;
                padding: 0 1rem;
            }
            .header-content h1 {
                margin: 0;
                font-size: 2rem;
            }
            .header-content p {
                margin: 0;
                font-size: 1rem;
                color: #e1e1e1;
            }
            .login-form {
                display: flex;
                flex-direction: column;
                width: 90%;
                max-width: 400px;
                padding: 2rem;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                text-align: center;
                margin-top: 80px;
            }
            .login-form input {
                width: 100%;
                padding: 0.75rem;
                margin-bottom: 1rem;
                border-radius: 8px;
                border: 1px solid #ddd;
                box-sizing: border-box;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s, box-shadow 0.3s;
            }
            .login-form input:focus {
                border-color: #007BFF;
                box-shadow: 0 0 8px rgba(0,123,255,0.5);
            }
            .login-form button {
                width: 100%;
                padding: 0.75rem;
                border: none;
                border-radius: 8px;
                background-color: #007BFF;
                color: #fff;
                font-size: 18px;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.2s;
            }
            .login-form button:hover {
                background-color: #0056b3;
                transform: scale(1.02);
            }
            .register-button {
                margin-top: 1rem;
                padding: 0.75rem;
                border: none;
                border-radius: 8px;
                background-color: #28a745;
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: background-color 0.3s, transform 0.2s;
            }
            .register-button:hover {
                background-color: #218838;
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
                <h1>Bienvenido a Bienes Raíces</h1>
                <p>Inicie sesión para continuar</p>
            </div>
        </header>
        <div class="login-form">
            <form method="POST">
                <input type="email" name="email" placeholder="Correo Electrónico" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Iniciar Sesión</button>
            </form>
            <a href="/register" class="register-button">Registrarse</a>
            <p>Credenciales incorrectas. <a href="/login">Volver</a></p>
        </div>
        <footer>
            <p>&copy; 2024 Bienes Raíces</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)
