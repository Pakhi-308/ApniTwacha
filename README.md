# 🌿 ApniTwacha

**Skin that glows from the inside out.**

ApniTwacha is an AI-powered skincare web app that analyses a user's photo, detects their skin type and key concerns using on-device deep learning models, and returns a personalised report — complete with home remedies (*Gharelu Nuskhe*), curated product suggestions, and a daily skincare routine.

🔗 **Live Demo:** [apnitwachafrontend.s3-website.ap-south-1.amazonaws.com](http://apnitwachafrontend.s3-website.ap-south-1.amazonaws.com)

🎥 **Demo Video:** [Watch here](https://drive.google.com/file/d/1f88c7_4VQNU8dW81_iR5b4tKOYTCQ16e/view?usp=sharing) <!-- TODO: replace with your actual Drive link -->

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
</details>

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
- HTML5, CSS3, vanilla JavaScript
- All markup, styling, and logic currently live together in a single `index.html` file (inline `<style>` and `<script>` blocks) rather than separate `.css`/`.js` files
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

| Model | Architecture | Validation/Test Accuracy | Dataset Size |
|---|---|---|---|
| Skin Type Classifier | EfficientNetB0 (fine-tuned, transfer learning) | **69.93%** (test set) | 4,093 images total — 2,872 train / 812 validation / 409 test |
| Concern Detection Model | EfficientNetB0 (multi-label, sigmoid output) | **69.93%** (test set) | 150 images (labeled metadata) |

> Verified directly from the training notebook (`Model_training.ipynb`). The skin type classifier went through several iterations — MobileNetV2 (frozen: 51.8%, fine-tuned: 57.7%) before switching to EfficientNetB0, which is the version actually exported to `skin_type_model.tflite`. Every live scan also returns a real-time per-image confidence score, shown to the user as "AI Accuracy" for that specific analysis.

**Inference pipeline:**
1. Uploaded photo → resized to 224×224 → converted to a float32 tensor
2. Passed through both TFLite interpreters independently
3. Skin type model → softmax confidence per class
4. Concern model → per-concern severity score → mapped to Low / Medium / High

---

## 🏗️ Architecture

```text
┌──────────────┐        ┌──────────────────┐        ┌───────────────────┐
│   Frontend   │──POST─▶│  Flask API       │──────▶│  TFLite Models    │
│ (S3 static)  │        │                  │        │  (skin_type +     │
│              │◀──JSON─│                  │◀──────│   concern)        │
└──────────────┘        └─────────┬────────┘        └───────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │    AWS S3        │
                        │ (user photos)    │
                        └──────────────────┘
