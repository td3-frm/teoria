import requests

# URL del endpoint (ajustá el puerto o dominio según corresponda)
url = "http://localhost:5000/sensor/configure"

# Datos de configuración a enviar (JSON)
payload = {
    "sensor_id": "SENSOR_5555",
    "temperature_limit": 75
}

# Encabezados HTTP
headers = {
    "Content-Type": "application/json"
}

try:
    # Enviar la solicitud POST
    response = requests.post(url, json=payload, headers=headers)

    # Mostrar el código de estado y la respuesta del servidor
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Error en la conexión: {e}")
