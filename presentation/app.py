from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
ANALYZER_SERVICE = "http://analyzer:5000/analyze"

@app.route("/present", methods=["POST"])
def present():
    payload = request.json or {}
    code = payload.get("code")
    if not code:
        return jsonify({"error":"no code provided"}), 400

    try:
        # Step 1: Send code to Analyzer
        resp = requests.post(ANALYZER_SERVICE, json={"code": code}, timeout=6)
        analysis = resp.json()
    except Exception as e:
        return jsonify({"error":"could not reach analyzer", "detail": str(e)}), 500

    # Step 2: Extract recurrence solution if available
    recurrence_solution = analysis.get("recurrence_solution", {})
    solution_data = recurrence_solution.get("solution", {})

    # Step 3: Fill big_o using recurrence solution if available
    if solution_data.get("theta"):
        big_o = solution_data["theta"]
    else:
        big_o = analysis.get("big_o_hint", "unknown")

    formatted = {
        "big_o": big_o,
        "explanation": "The recurrence was analyzed using the Recurrence service. See recurrence_solution for step-by-step details.",
        "recurrence_analysis": recurrence_solution
    }

    return jsonify({"analysis": formatted, "raw": analysis})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

