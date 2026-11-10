# MessWise — Vercel Edition

A separately designed Vercel version of the University Mess Food Demand & Waste Prediction System. The original Streamlit app is not modified.

## Design direction
This edition uses a custom editorial-style interface: horizontal top tabs (no sidebar), a landing-page hero, compact metric tiles, a two-column prediction studio, and separate model/project pages. It is intentionally not a Streamlit dashboard skin.

## Architecture
- Static frontend: HTML, CSS and JavaScript
- Serverless prediction endpoint: Vercel Python Function at `api/predict.py`
- Model artifacts: the existing trained Scikit-learn demand and waste pipelines
- No model retraining occurs during a web request

## Run locally
Use Python 3.11 and a compatible scikit-learn environment.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install vercel
vercel dev
```
Open the local URL printed by Vercel CLI.

## Deploy to Vercel
1. Create a **new** GitHub repository, for example `University-MessWise-Vercel`.
2. Upload the contents of this folder (the `index.html`, `api`, `models`, `assets`, `style.css`, `app.js`, `requirements.txt`, `vercel.json` and README) to the repository root.
3. In Vercel, choose **Add New → Project** and import this new repository.
4. Keep the project root directory as `./` and deploy. No build command is required for the static frontend.
5. Open the deployed site and test the Prediction Studio. The API health endpoint is `/api/predict`.

If Vercel asks for a Python version, use Python 3.12 or the currently supported version shown by Vercel. If the Python dependency build fails, check Vercel's current Python runtime documentation and align the runtime and scikit-learn versions.

## Prediction input fields
Meal type, day, weather, menu category, weekend flag, holiday flag, exam-period flag, expected students and planned portions. Weekend is derived from the selected day. The backend uses the existing `demand_model` and `waste_model` objects from the supplied Joblib bundle.

## Academic transparency
The attached data and trained models are based on a **synthetic simulated dataset**, not actual university mess records. The reported metrics are academic demonstration results and do not prove real-world food waste reduction. Real operational use requires consented real records, retraining and validation.

## Existing Streamlit deployment
Keep your current Streamlit deployment and repository unchanged. This Vercel edition is designed to be deployed as a separate project/repository.
