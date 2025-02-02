from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g,make_response
import requests
import googlemaps

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/incidente_create_view')
def render_generar_incidentes():
    return render_template('incidente_create_view.html')

CLOUD_RUN_API_URL = "https://gateway-incidente-create-5s8gqz3e.ue.gateway.dev/api/incidente_create"



@app.route('/incidente_create', methods=['POST'])
def incidente_create():
    """
    Recibe los datos del formulario HTML y los reenvía a la API de Cloud Run, 
    incluyendo la cookie segura `jwt_token` en la cabecera Authorization.
    """
    try:
        data = request.json  # Recibe los datos en formato JSON desde el frontend
        jwt_token = request.headers.get("Authorization")  # Captura el token de la cabecera
        
        if not jwt_token:
            return jsonify({"error": "No autorizado. Falta el token JWT"}), 401

        # Enviar la petición a Cloud Run con el token JWT
        response = requests.post(
            CLOUD_RUN_API_URL,
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": jwt_token  # Pasar el token al backend
            }
        )

        response_data = response.json()

        if response.status_code in [200, 201]:
            return jsonify({"message": "Incidente enviado con éxito", "id": response_data.get("id")})
        else:
            return jsonify({"error": response_data}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Error al conectar con Cloud Run: {str(e)}"}), 500









#########################################################################


# Inicializa el cliente de Google Maps
API_KEY = "AIzaSyCGEtHtLt3VXK_FX7nCUXphfbVVeSoFyto"
gmaps = googlemaps.Client(key=API_KEY)

# Coordenadas de los límites (bounding box) del GeoJSON
san_miguel_bounds = {
    "northeast": {"lat": -34.512225550529806, "lng": -58.638687300296965},
    "southwest": {"lat": -34.62334078576083, "lng": -58.78663729083311},
}

# Calcular el centro del bounding box
san_miguel_location = {
    "lat": (san_miguel_bounds["northeast"]["lat"] + san_miguel_bounds["southwest"]["lat"]) / 2,
    "lng": (san_miguel_bounds["northeast"]["lng"] + san_miguel_bounds["southwest"]["lng"]) / 2,
}


# Ruta 1: Autocomplete
@app.route('/gmaps', methods=['GET'])
def proxy_gmaps():
    try:
        # Obtener el parámetro de entrada desde el cliente
        input_value = request.args.get('input', '')
        print(f"[DEBUG] Parámetro 'input' recibido: {input_value}")

        if not input_value:
            print("[DEBUG] Parámetro 'input' faltante.")
            return jsonify({"error": "El parámetro 'input' es obligatorio"}), 400

        # Llamar a la API de Google Maps Autocomplete
        print("[DEBUG] Realizando solicitud a Google Maps Autocomplete...")
        autocomplete_result = gmaps.places_autocomplete(
            input_value,
            location=(san_miguel_location['lat'], san_miguel_location['lng']),
            radius=5000,  # Radio en metros
            strict_bounds=True  # Limitar estrictamente al área definida
        )

        # Depuración de los resultados
        print(f"[DEBUG] Respuesta de Google Maps Autocomplete: {autocomplete_result}")

        if not autocomplete_result:
            print("[DEBUG] No se encontraron resultados para el input proporcionado.")
            return jsonify({"error": "No se encontraron sugerencias"}), 404

        # Devolver el resultado al cliente
        print("[DEBUG] Enviando sugerencias al cliente.")
        return jsonify({"predictions": autocomplete_result})

    except Exception as e:
        print(f"[ERROR] Excepción ocurriendo en /gmaps: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Ruta 2: Place Details
@app.route('/gmaps/place/details/json', methods=['GET'])
def proxy_gmaps_place_details():
    try:
        # Obtener el parámetro `place_id` desde el cliente
        place_id = request.args.get('place_id', '')
        print(f"[DEBUG] Parámetro place_id recibido: {place_id}")  # Depuración del parámetro recibido

        if not place_id:
            print("[DEBUG] Falta el parámetro 'place_id'.")
            return jsonify({"error": "El parámetro 'place_id' es obligatorio"}), 400

        # Llamar a la API de Google Maps para obtener detalles del lugar
        print(f"[DEBUG] Realizando solicitud a Google Maps con place_id: {place_id}")
        place_details = gmaps.place(place_id=place_id)

        # Depuración de la respuesta de Google Maps
        print(f"[DEBUG] Respuesta de Google Maps: {place_details}")

        # Verificar si la respuesta contiene resultados
        if "result" in place_details:
            print("[DEBUG] Detalles del lugar encontrados. Enviando respuesta al cliente.")
            return jsonify(place_details)
        else:
            print("[DEBUG] No se encontraron detalles para el place_id proporcionado.")
            return jsonify({"error": "No se encontraron detalles para el lugar especificado"}), 404

    except Exception as e:
        print(f"[ERROR] Excepción ocurriendo en /gmaps/place/details/json: {str(e)}")
        return jsonify({"error": str(e)}), 500











AUTH_API_URL = "https://auth-login-453282587690.southamerica-east1.run.app/api/auth/login"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Enviar credenciales a la API de autenticación
        response = requests.post(AUTH_API_URL, json={"email": email, "password": password})
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            rol = data.get("rol")
            background = data.get("background_color_prefered")

            if token:
                # Guardar token y preferencias en cookies seguras
                resp = make_response(redirect("/"))
                resp.set_cookie("jwt_token", token, httponly=False, secure=True, samesite="Lax")
                resp.set_cookie("rol", rol, secure=True, samesite="Lax")
                resp.set_cookie("background", background, secure=True, samesite="Lax")
                return resp
            else:
                return render_template("login.html", error="Invalid response from server")

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
