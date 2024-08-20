from pymongo import MongoClient, errors

MONGO_URI = "mongodb+srv://msolano80258:Francia9192@cluster0.6uxqadh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class MongoDBConnection:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client['ProyectoNosql']  
            print("Conexión a MongoDB exitosa")
        except errors.ConnectionError as e:
            print(f"Error al conectar a MongoDB: {e}")
        except errors.PyMongoError as e:
            print(f"Error en la operación de MongoDB: {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]
