<?php
class Client {
    private $uri;
    private $database;
    private $collection;

    public function __construct($uri) {
        $this->uri = $uri;
    }

    public function selectDatabase($databaseName) {
        $this->database = $databaseName;
        return $this;
    }

    public function selectCollection($collectionName) {
        $this->collection = $collectionName;
        return $this;
    }

    private function request($method, $endpoint, $data = null) {
        $url = "https://$this->uri/$this->database/$this->collection$endpoint";
        $ch = curl_init($url);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Basic ' . base64_encode('username:password') // Ajusta según tus credenciales
        ]);

        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }

        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

        $response = curl_exec($ch);
        if (curl_errno($ch)) {
            throw new Exception('Error en la solicitud: ' . curl_error($ch));
        }
        curl_close($ch);

        return json_decode($response, true);
    }

    public function listCollections() {
        return $this->request('GET', '/listCollections');
    }

    public function find() {
        return $this->request('GET', '/find');
    }

    public function toArray($data) {
        return $data;
    }
}
?>
