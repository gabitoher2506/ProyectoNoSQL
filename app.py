from flask import Flask

app = Flask(__name__)

# Importar las rutas desde los archivos separados
from index import *
from details import *
from contacto import *

if __name__ == '__main__':
    app.run(debug=True)
