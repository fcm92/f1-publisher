# f1_proxy_publisher.py
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json

    # Verificações básicas
    if not data or not all(k in data for k in ("wp_url", "username", "app_password", "title", "content")):
        return jsonify({"error": "Missing required fields."}), 400

    wp_url = data["wp_url"].rstrip("/") + "/wp-json/wp/v2/posts"
    auth = (data["username"], data["app_password"])
    post_data = {
        "title": data["title"],
        "content": data["content"],
        "status": "publish"
    }

    try:
        response = requests.post(wp_url, json=post_data, auth=auth)
        if response.status_code == 201:
            return jsonify({"message": "✅ Post published!", "url": response.json().get("link")}), 201
        else:
            return jsonify({"error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
