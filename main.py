from flask_cors import CORS
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
CORS(app, resources={r"/run": {"origins": "*"}})

PISTON_URL = "https://piston.rs/api/v2/execute"

@app.route("/run", methods=["POST"])
def run_code():
    try:
        data = request.json
        print("Received payload:", data)  # ✅ Log incoming request

        language = data.get("language")
        version = data.get("version")
        code = data.get("code")
        stdin = data.get("stdin", "")
        extension = data.get("extension", ".txt")

        payload = {
            "language": language,
            "version": version,
            "files": [{"name": f"main{extension}", "content": code}],
            "stdin": stdin
        }

        print("Sending to Piston:", payload)  # ✅ Log what you're sending

        piston_response = requests.post(PISTON_URL, json=payload, timeout=10)
        piston_response.raise_for_status()
        print("Piston response:", piston_response.json())  # ✅ Log response

        return jsonify(piston_response.json())

    except requests.RequestException as e:
        print("Request error:", str(e))  # ✅ Print exact request error
        return jsonify({"error": "Execution failed", "details": str(e)}), 500
    except Exception as e:
        print("Unhandled error:", str(e))  # ✅ Catch any other errors
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
