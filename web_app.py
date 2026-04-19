"""
ClearCom web interface.
Run with: python web_app.py
"""

from flask import Flask, jsonify, render_template, request

from compiler_service import compile_source


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/compile")
def api_compile():
    payload = request.get_json(silent=True) or {}
    source_code = payload.get("source", "")

    if not source_code.strip():
        return jsonify({"success": False, "errors": ["No source code provided."]}), 400

    result = compile_source(source_code)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
