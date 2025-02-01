from flask import Flask, render_template, request, jsonify
import googlemaps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Página principal
@app.route('/')
def render_generar_incidentes():
    return render_template('incidente_create_view.html')

# Inicializa el cliente de Google Maps
API_KEY = "AIzaSyCGEtHtLt3VXK_FX7nCUXphfbVVeSoFyto"
gmaps = googlemaps.Client(key=API_KEY)

# Coordenadas de San Miguel (Bounding Box)
san_miguel_location = {
    "lat": -34.56778316814532,
    "lng": -58.71266229556504
}

# 🔹 Ruta 1: Autocomplete (Obtención de sugerencias de lugares)
@app.route('/gmaps/autocomplete', methods=['GET'])
def gmaps_autocomplete():
    input_value = request.args.get('input', '')

    if not input_value:
        return jsonify({"error": "El parámetro 'input' es obligatorio"}), 400

    try:
        autocomplete_result = gmaps.places_autocomplete(
            input_value,
            location=(san_miguel_location['lat'], san_miguel_location['lng']),
            radius=5000,
            strict_bounds=True
        )

        if not autocomplete_result:
            return jsonify({"error": "No se encontraron sugerencias"}), 404

        return jsonify({"predictions": autocomplete_result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔹 Ruta 2: Place Details (Detalles de un lugar específico)
@app.route('/gmaps/place/details', methods=['GET'])
def gmaps_place_details():
    place_id = request.args.get('place_id', '')

    if not place_id:
        return jsonify({"error": "El parámetro 'place_id' es obligatorio"}), 400

    try:
        place_details = gmaps.place(place_id=place_id)

        if "result" in place_details:
            return jsonify(place_details)
        else:
            return jsonify({"error": "No se encontraron detalles para el lugar especificado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
