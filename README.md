# 🌿 ApniTwacha

**Skin that glows from the inside out.**

ApniTwacha is an AI-powered skincare web app that analyses a user's photo, detects their skin type and key concerns using on-device deep learning models, and returns a personalised report — complete with home remedies (*Gharelu Nuskhe*), curated product suggestions, and a daily skincare routine.

🔗 **Live Demo:** [apnitwachafrontend.s3-website.ap-south-1.amazonaws.com](http://apnitwachafrontend.s3-website.ap-south-1.amazonaws.com)

🎥 **Demo Video:** [Watch here](https://drive.google.com/PLACEHOLDER_REPLACE_WITH_YOUR_DRIVE_LINK) <!-- TODO: replace with your actual Drive link -->

---

## 📸 Screenshots

<details open>
<summary><strong>1. Welcome / Personalisation</strong></summary>
<br>
<img src="https://github.com/user-attachments/assets/4e519bef-8a4b-4246-a811-10cb8218f5f1" width="700"/>
</details>

<details>
<summary><strong>2. Personalised Skin Report</strong></summary>
<br>
<img src="https://github.com/user-attachments/assets/f7ed93ca-f861-4cfd-a40b-5d467e65672b" width="700"/>

<details>
<summary><strong>3. Home Remedies & Product Recommendations</strong></summary>
<br>
<img src="https://github.com/user-attachments/assets/bcc389c8-d904-4d75-b009-e23d38410905" width="700"/>
</details>

<details>
<summary><strong>4. Daily Routine</strong></summary>
<br>
<img src="https://github.com/user-attachments/assets/f2cd507a-444a-428c-b5f1-025acff602ba" width="700"/>
</details>

---

## ✨ Features

- 📷 **AI Skin Analysis** — upload a selfie and get instant skin type + concern detection
- 🧴 **Personalised Report** — skin type, top concern, severity level, and confidence score
- 🌿 **Gharelu Nuskhe** — natural home remedies tailored to the detected skin type
- 🛍️ **Curated Product Recommendations** — cleanser, serum, SPF, and treatment suggestions
- 📅 **Daily Routine Builder** — morning & night skincare steps
- 👋 **Personalised Welcome** — user enters their name so the experience feels tailored to them
- ☁️ **Cloud-Native** — photos uploaded to **AWS S3**, backend served via AWS

### 🚧 Planned / In Progress
- 🕒 **Skin History Tracking** — viewing past scans and skin transformation over time (not yet implemented)

---

## 🛠️ Tech Stack

**Frontend**
- HTML5, CSS3, vanilla JavaScript (no framework)
- Fetch API for backend communication
- Hosted as a static site on **AWS S3**

**Backend**
- Python + Flask (REST API)
- Flask-CORS for cross-origin requests
- TensorFlow Lite Runtime (`tf.lite.Interpreter`) for model inference
- Pillow (PIL) + NumPy for image preprocessing

**Data & Storage**
- **AWS S3** — stores user-uploaded skin photos

**AI / Machine Learning**
- Two independent CNN models, trained on **Google Colab** and exported to **TensorFlow Lite** for fast, lightweight CPU inference
- Image input: 224×224 RGB, normalized via PIL/NumPy before inference

---

## 🧠 AI Models

| Model | Purpose | Output |
|---|---|---|
| `skin_type_model.tflite` | Classifies overall skin type | 4 classes: `combination`, `dry`, `normal`, `oily` |
| `concern_model.tflite` | Detects specific skin concerns | 5 severity scores (0–5): Acne, Redness, Excess Oil, Dark Spots, Dehydration |

**Accuracy:**

| Model | Validation Accuracy | Dataset Size |
|---|---|---|
| Skin Type Classifier | `TODO — add your val_accuracy from the Colab training run` | `TODO` |
| Concern Detection Model | `TODO — add your val_accuracy from the Colab training run` | `TODO` |

> Both models were trained once on Google Colab. The `.tflite` files themselves don't store training metrics, so pull the final `val_accuracy` from your Colab notebook's training output/history and drop it in above. Every live scan also returns a real-time per-image confidence score, shown to the user as "AI Accuracy" for that specific analysis.

**Inference pipeline:**
1. Uploaded photo → resized to 224×224 → converted to a float32 tensor
2. Passed through both TFLite interpreters independently
3. Skin type model → softmax confidence per class
4. Concern model → per-concern severity score → mapped to Low / Medium / High

---

## 🏗️ Architecture

```
┌──────────────┐        ┌──────────────────┐        ┌───────────────────┐
│   Frontend   │──POST─▶│  Flask API        │──────▶│  TFLite Models     │
│ (S3 static)  │        │                   │        │  (skin_type +      │
│              │◀──JSON─│                   │◀──────│   concern)         │
└──────────────┘        └─────────┬─────────┘        └───────────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │   AWS S3          │
                          │ (user photos)     │
                          └──────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip
- An AWS account (S3 bucket, if deploying yourself)

### Backend Setup

```bash
# clone the repo
git clone https://github.com/<your-username>/apnitwacha.git
cd apnitwacha/backend

# install dependencies
pip install flask flask-cors tensorflow pillow numpy

# make sure your models are in place
# backend/models/skin_type_model.tflite
# backend/models/concern_model.tflite
# backend/models/skin_type_labels.json
# backend/models/concern_labels.json

# run the server
python app.py
```

The API will start on `http://127.0.0.1:5000`.

### Frontend Setup

The frontend is a static `index.html` — no build step required.

```bash
cd frontend
# open directly in a browser, or serve locally:
python -m http.server 5500
```

Update the `API_BASE` constant near the top of the `<script>` block in `index.html` to point at your backend URL (local Flask server or your deployed endpoint).

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analyze` | Upload a photo + form data (gender, age, concerns), get skin type + concern analysis |

---

## 📁 Project Structure

```
apnitwacha/
├── backend/
│   ├── app.py
│   ├── models/
│   │   ├── skin_type_model.tflite
│   │   ├── concern_model.tflite
│   │   ├── skin_type_labels.json
│   │   └── concern_labels.json
│   └── uploads/
├── frontend/
│   └── index.html
├── assets/
│   └── screenshots/
└── README.md
```

---

## 🤝 Contributing

Contributions are what make the open-source community amazing — any contributions you make are **greatly appreciated**.

1. **Fork** the repository
2. **Create your feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add: AmazingFeature"
   ```
4. **Push to your branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request** describing what you changed and why

### Ways to contribute
- 🐛 Report bugs by opening an [issue](../../issues)
- 💡 Suggest new features (better remedy logic, more skin concerns, UI polish)
- 🧠 Improve model accuracy or add new training data
- 📝 Improve documentation
- 🎨 Enhance frontend design / accessibility
- 🕒 Help build out the skin history tracking feature

### Guidelines
- Keep PRs focused — one feature/fix per PR
- Follow existing code style (PEP8 for Python, consistent naming in JS)
- Test your changes locally before submitting
- Be respectful and constructive in code reviews

---

## 🙋 Author

Built with 🌿 by **Pakhi Shukla**
Feel free to reach out for collaboration or questions.
