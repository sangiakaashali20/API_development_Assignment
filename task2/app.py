from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Generate three unique API keys
API_KEYS = {
    secrets.token_urlsafe(24): "Consumer 1",
    secrets.token_urlsafe(24): "Consumer 2",
    secrets.token_urlsafe(24): "Consumer 3"
}

# Show keys in the terminal for classroom testing only
print("\n=== API KEYS: SHARE PRIVATELY ===")
for key, consumer in API_KEYS.items():
    print(f"{consumer}: {key}")
print("=================================\n")


@app.route("/process", methods=["POST"])
def process_text():
    # Validate the API key
    api_key = request.headers.get("X-API-Key")

    if not api_key or api_key not in API_KEYS:
        return jsonify({"error": "Invalid or missing API key"}), 401

    # Read JSON input
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("text"), str):
        return jsonify({"error": "Please provide text as a JSON string"}), 400

    # Process the text
    processed_text = data["text"].upper()

    return jsonify({
        "consumer": API_KEYS[api_key],
        "original_text": data["text"],
        "processed_text": processed_text
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)