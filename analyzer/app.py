from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)
RECURRENCE_SERVICE = "http://recurrence:5001/solve"

def naive_detect_recurrence(code: str):
    s = code.replace(" ", "")
    m = re.search(r"T\(n\)\s*=\s*(\d+)T\(n/(\d+)\)\+(.+)", s)
    if m:
        a, b, f = m.groups()
        return {"type":"divide-and-conquer", "a":int(a), "b":int(b), "f":f}
    if re.search(r"for\s+\w+\s+in\s+range|while\s*\(", code):
        return {"type":"loop", "hint":"may be O(n) or O(n^2) depending on nested loops"}
    return {"type":"unknown"}

@app.route("/analyze", methods=["POST"])
def analyze():
    payload = request.json or {}
    code = payload.get("code", "")
    if not code:
        return jsonify({"error":"no code provided"}), 400

    rec = naive_detect_recurrence(code)
    result = {"recurrence_detected": rec}

    if rec.get("type") == "divide-and-conquer":
        try:
            resp = requests.post(RECURRENCE_SERVICE, json={
                "a": rec["a"], "b": rec["b"], "f": rec["f"]
            }, timeout=5)
            result["recurrence_solution"] = resp.json()
        except Exception as e:
            result["recurrence_solution"] = {"error":"could not reach recurrence service", "detail": str(e)}

    if rec.get("type") == "loop":
        result["big_o_hint"] = "O(n) or O(n^2) - check nested loops."
    elif rec.get("type") == "divide-and-conquer":
        result["big_o_hint"] = "Use recurrence solution returned above."
    else:
        result["big_o_hint"] = "unknown"

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
