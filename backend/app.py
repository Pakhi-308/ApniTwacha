from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
MODEL_FOLDER = "models"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------------
# Load models once at startup
# -------------------------------

skin_interpreter = tf.lite.Interpreter(model_path=os.path.join(MODEL_FOLDER, "skin_type_model.tflite"))
skin_interpreter.allocate_tensors()

concern_interpreter = tf.lite.Interpreter(model_path=os.path.join(MODEL_FOLDER, "concern_model.tflite"))
concern_interpreter.allocate_tensors()

with open(os.path.join(MODEL_FOLDER, "skin_type_labels.json")) as f:
    skin_labels = json.load(f)

with open(os.path.join(MODEL_FOLDER, "concern_labels.json")) as f:
    concern_labels = json.load(f)

skin_input_details = skin_interpreter.get_input_details()
skin_output_details = skin_interpreter.get_output_details()

concern_input_details = concern_interpreter.get_input_details()
concern_output_details = concern_interpreter.get_output_details()


def preprocess_image(image_path, size=(224, 224)):
    img = Image.open(image_path).convert("RGB").resize(size)
    arr = np.array(img, dtype=np.float32)
    return np.expand_dims(arr, axis=0)


def predict_skin_type(input_data):
    skin_interpreter.set_tensor(skin_input_details[0]["index"], input_data)
    skin_interpreter.invoke()
    output = skin_interpreter.get_tensor(skin_output_details[0]["index"])[0]
    idx = int(np.argmax(output))
    return skin_labels[idx], float(output[idx])


def predict_concerns(input_data):
    concern_interpreter.set_tensor(concern_input_details[0]["index"], input_data)
    concern_interpreter.invoke()
    output = concern_interpreter.get_tensor(concern_output_details[0]["index"])[0]
    return dict(zip(concern_labels, output.tolist()))


def severity_from_score(score):
    if score >= 0.75:
        return "High"
    elif score >= 0.5:
        return "Medium"
    else:
        return "Low"


@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    gender = request.form.get("gender")
    age = request.form.get("age")
    concerns_input = request.form.get("concerns")

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # -------------------------------
    # Real AI Prediction
    # -------------------------------

    input_data = preprocess_image(image_path)

    skin_type, skin_confidence = predict_skin_type(input_data)
    concern_scores = predict_concerns(input_data)

    # pick the top concern by score
    top_concern = max(concern_scores, key=concern_scores.get)
    top_concern_score = concern_scores[top_concern]

    result = {
        "skin_type": skin_type,
        "concern": top_concern,
        "confidence": f"{round(skin_confidence * 100)}%",
        "severity": severity_from_score(top_concern_score),
        "all_concerns": {
            k: {
                "score": round(v, 2),
                "present": v >= 0.5
            } for k, v in concern_scores.items()
        }
    }

    print("Gender :", gender)
    print("Age :", age)
    print("Concerns :", concerns_input)
    print("Result:", result)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
