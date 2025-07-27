from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PISTON_URL = "https://piston.rs/api/v2/execute"

@app.route("/run", methods=["POST"])
def run_code():
    data = request.json
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

    try:
        piston_response = requests.post(PISTON_API_URL, json=payload)
        piston_response.raise_for_status()
        return jsonify(piston_response.json())
    except requests.RequestException as e:
        return jsonify({"error": "Execution failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
