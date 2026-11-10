from http.server import BaseHTTPRequestHandler
from pathlib import Path
import json, joblib

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "mess_prediction_models.joblib"
_models = None

def get_models():
    global _models
    if _models is None:
        _models = joblib.load(MODEL_PATH)
    return _models

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            required = ["meal_type","day_of_week","weather","menu_category","is_weekend","is_holiday","exam_period","expected_students","portions_prepared"]
            missing = [k for k in required if k not in payload]
            if missing:
                return self.respond(400, {"error":"Missing fields: " + ", ".join(missing)})
            import pandas as pd
            row = {k: payload[k] for k in required}
            demand_row = pd.DataFrame([{k: row[k] for k in required if k != "portions_prepared"}])
            waste_row = demand_row.copy()
            waste_row["portions_prepared"] = int(row["portions_prepared"])
            models = get_models()
            demand = max(0, int(round(float(models["demand_model"].predict(demand_row)[0]))))
            waste = max(0, int(round(float(models["waste_model"].predict(waste_row)[0]))))
            prepared = int(row["portions_prepared"])
            waste = min(waste, prepared)
            suggested = min(900, max(0, int(round(demand * 1.04))))
            return self.respond(200, {"predicted_demand": demand, "suggested_preparation": suggested,
                                      "estimated_waste": waste, "planned_portions": prepared,
                                      "difference": prepared-demand})
        except Exception as exc:
            return self.respond(500, {"error": "Prediction could not be generated. " + str(exc)})
    def do_GET(self):
        return self.respond(200, {"status":"ok","service":"MessWise prediction API"})
    def respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)
    def do_OPTIONS(self):
        return self.respond(200, {"ok":True})
