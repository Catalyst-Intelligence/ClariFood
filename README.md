# 🥑 ClariFood: Conversational Diet Intelligence Platform

ClariFood is an advanced, containerized dietary analysis platform designed to process nutritional data and food packaging through hybrid computer vision and multimodal Large Language Models (LLMs). Built with a modular micro-service architecture, the system leverages Google's Gemini Flash runtime API alongside custom processing pipelines to safely deliver automated nutritional feedback.

---

## 🚀 Live Deployments
You can checkout the live working product from the Production Sandbox link given below.
* **Production Sandbox Slot:** [catalyst-intelligence-clarifood.hf.space](https://catalyst-intelligence-clarifood.hf.space/)

* **Isolated Staging Track (for beta testing only):** [staging-clarifood.hf.space](https://staging-clarifood.hf.space/)

## ⚙️ System Architecture & Stack
* **Frontend Framework:** Streamlit (Python-native UI engine)
* **Intelligence Layer:** Google Gemini 2.5 API (Multimodal token parsing)
* **Containerization:** Docker (`python:3.10-slim` base layers)
* **CI/CD Automation:** GitHub Actions infrastructure (Matrix branch deployments using modern `hf` upload protocols)
* **System Utilities:** Ubuntu Linux C++ runtime dependencies (`libzbar0` for barcode handling, `libgl1-mesa-glx` for headless OpenCV rendering graphics)

## 📦 Local Workspace Installation
To activate and scale this codebase inside a local environment, clone the repository and initialize via Anaconda:

```bash
# Clone the repository
git clone [https://github.com/Catalyst-Intelligence/ClariFood.git](https://github.com/Catalyst-Intelligence/ClariFood.git)
cd ClariFood

# Create and activate local environment
conda create -n clarifood_env python=3.10 -y
conda activate clarifood_env

# Install structural dependencies
pip install -r requirements.txt

# Run local hot-reload tracking server
streamlit run app.py