from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Fake database (for demo)
products = [
    {
        "id": 1,
        "name": "Chocolate Cake",
        "price": 20,
        "imageUrl": "https://via.placeholder.com/150"
    },
    {
        "id": 2,
        "name": "Vanilla Cake",
        "price": 18,
        "imageUrl": "https://via.placeholder.com/150"
    },
    {
        "id": 3,
        "name": "Strawberry Cake",
        "price": 22,
        "imageUrl": "https://via.placeholder.com/150"
    }
]

registrations = []


# ✅ THIS IS WHAT YOU WERE MISSING
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/register-class", methods=["POST"])
def register_class():
    data = request.get_json()

    if not data.get("name") or not data.get("phone"):
        return {"error": "Missing required fields"}, 400

    registrations.append(data)

    return {
        "message": "Registration successful",
        "data": data
    }, 201

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename, cache_timeout=3600)  # 1 hour
    r
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)