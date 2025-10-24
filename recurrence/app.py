from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def master_theorem(a, b, f_str):
    try:
        a = int(a); b = int(b)
    except:
        return {"error":"a and b must be integers"}
    log_term = math.log(a, b)
    import re
    m = re.search(r"n\^(\d+)", f_str)
    if m:
        c = int(m.group(1))
        if abs(c - log_term) < 1e-6:
            return {"theta": f"n^{c}", "case":"2 (f(n) = Theta(n^{log_b a}))"}
        elif c < log_term:
            return {"theta": f"n^{log_term:.3f}", "case":"1 (f(n) = O(n^{log_b a - eps}))"}
        else:
            return {"theta": f"f(n) dominates (approx n^{c})", "case":"3 (f(n) = Omega(n^{log_b a + eps}))"}
    return {"theta": f"n^{log_term:.3f} (master theorem baseline)", "note":"f(n) not parsed; returned baseline"}

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json or {}
    a = data.get("a")
    b = data.get("b")
    f = data.get("f", "unknown")
    if a is None or b is None:
        return jsonify({"error":"missing a or b"}), 400
    sol = master_theorem(a, b, str(f))
    return jsonify({"a":a, "b":b, "f":f, "solution": sol})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
