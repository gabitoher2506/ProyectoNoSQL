from flask import Flask, render_template_string
from pymongo import MongoClient

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
        # Crear una instancia de MongoDBConnection
        db_connection = MongoDBConnection()

        # Seleccionar la colección de propiedades
        property_collection = db_connection.get_collection('Property')

        # Realizar una consulta simple (ejemplo: obtener algunas propiedades)
        properties = property_collection.find().limit(6)  # Limita el número de propiedades para mostrar

        # Preparar HTML para mostrar propiedades
        property_list = ""
        for property in properties:
            # Obtener las imágenes asociadas a la propiedad
            image_ids = property.get('image_ids', [])
            images_collection = db_connection.get_collection('PropertyImages')
            images = images_collection.find({'_id': {'$in': image_ids}})
            image_urls = [image.get('image_url', 'placeholder.jpg') for image in images]

            # Preparar una lista de imágenes
            images_html = ""
            for url in image_urls:
                images_html += f'<img src="{url}" alt="Imagen de la propiedad">'

            property_list += f"""
            <div class="property">
                <div class="property-info">
                    <h2>{property.get('name', 'Nombre de la Propiedad')}</h2>
                    <p>{property.get('description', 'Descripción de la propiedad')}</p>
                    <p><strong>Precio:</strong> ${property.get('price', '0')}</p>
                    <div class="property-images">
                        {images_html}
                    </div>
                    <a href="/property/{property.get('_id')}">Ver más</a>
                </div>
            </div>
            """

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
                    {{ property_list|safe }}
                </div>
            </div>
            <footer>
                <p>&copy; 2024 Bienes Raíces. Todos los derechos reservados.</p>
            </footer>
        </body>
        </html>
        """
        db_connection.close()
        return render_template_string(html, property_list=property_list)

    except Exception as e:
        return f"Error en la operación de MongoDB: {e}"

if __name__ == '__main__':
    app.run(debug=True)
