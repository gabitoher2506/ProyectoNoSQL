<?php
require_once 'Client.php'; // Incluye el archivo que contiene la clase Client

// Cadena de conexión de MongoDB Atlas (sin usar MongoDB\Client)
$uri = "mongodb+srv://msolano80258:Francia9192@cluster0.6uxqadh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

try {
    // Crear el cliente
    $client = new Client($uri);

    // Seleccionar la base de datos
    $database = $client->selectDatabase('ProyectoNosql');

    // Listar colecciones
    $collections = $database->listCollections();
    echo '<h1>Colecciones en la Base de Datos</h1>';
    echo '<ul>';
    foreach ($collections as $collection) {
        echo '<li>' . htmlspecialchars($collection['name']) . '</li>';
    }
    echo '</ul>';

    // Seleccionar una colección para mostrar documentos
    $collectionName = 'Users'; // Reemplaza con el nombre de tu colección
    $database->selectCollection($collectionName);

    // Realizar una consulta simple (ejemplo: obtener todos los documentos)
    $documents = $database->find();
    $documentsArray = $client->toArray($documents);

    // Mostrar documentos
    echo '<h1>Documentos en la Colección ' . htmlspecialchars($collectionName) . '</h1>';
    if (empty($documentsArray)) {
        echo '<p>No se encontraron documentos en la colección.</p>';
    } else {
        echo '<pre>';
        print_r($documentsArray);
        echo '</pre>';
    }
} catch (Exception $e) {
    echo "Error al conectar a MongoDB: " . $e->getMessage();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prueba de Conexión a MongoDB</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .message {
            font-size: 18px;
            color: green;
        }
    </style>
</head>
<body>
    <h1>Prueba de Conexión a MongoDB</h1>
    <p class="message"><?php echo htmlspecialchars($message ?? ''); ?></p>
</body>
</html>
