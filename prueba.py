from flask import Flask, render_template_string
from pymongo import MongoClient, errors

app = Flask(__name__)

# URI de conexión a MongoDB Atlas
uri = "mongodb+srv://msolano80258:Francia9192@cluster0.6uxqadh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@app.route('/')
def index():
    try:
        # Crear el cliente MongoDB
        client = MongoClient(uri)
        print("Conexión a MongoDB exitosa")

        # Seleccionar la base de datos
        db = client['ProyectoNosql']  # Reemplaza con el nombre de tu base de datos

        # Seleccionar la colección
        collection = db['Address']  # Reemplaza con el nombre de tu colección

        # Realizar una consulta simple (ejemplo: obtener todos los documentos)
        documents = collection.find()

        # Preparar HTML para mostrar documentos
        doc_list = "<h1>Documentos en la Colección 'Users'</h1><ul>"
        for document in documents:
            doc_list += f"<li>{document}</li>"
        doc_list += "</ul>"

        return render_template_string(doc_list)

    except errors.ConnectionError as e:
        return f"Error al conectar a MongoDB: {e}"
    except errors.PyMongoError as e:
        return f"Error en la operación de MongoDB: {e}"

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    try:
        # Crear el cliente MongoDB
        client = MongoClient(uri)
        print("Conexión a MongoDB exitosa")

        # Seleccionar la base de datos
        db = client['ProyectoNosql']  # Reemplaza con el nombre de tu base de datos

        # Seleccionar la colección
        collection = db['Users']  # Reemplaza con el nombre de tu colección

        # Realizar una consulta simple (ejemplo: obtener todos los documentos)
        documents = collection.find()

        # Preparar HTML para mostrar documentos
        doc_list = "<h1>Documentos en la Colección 'Users'</h1><ul>"
        for document in documents:
            doc_list += f"<li>{document}</li>"
        doc_list += "</ul>"

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test de Conexión a MongoDB</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                .message {
                    font-size: 18px;
                    color: green;
                }
                pre {
                    background: #f4f4f4;
                    padding: 10px;
                    border: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <h1>Test de Conexión a MongoDB</h1>
            <h2>Documentos en la Colección 'Users'</h2>
            <pre>{{ documents_list }}</pre>
        </body>
        </html>
        """, documents_list=doc_list)

    except errors.ConnectionError as e:
        return f"Error al conectar a MongoDB: {e}"
    except errors.PyMongoError as e:
        return f"Error en la operación de MongoDB: {e}"

if __name__ == '__main__':
    app.run(debug=True)
