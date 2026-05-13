from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_skin():

    image = request.files.get('image')

    if not image:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    result = {
        "skin_type": "Oily",
        "concern": "Acne",
        "confidence": "94%"
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 