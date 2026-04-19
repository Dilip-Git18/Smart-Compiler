"""
ClearCom web interface.
Run with: python web_app.py
"""

import time

from flask import Flask, jsonify, render_template, request

from compiler_service import compile_source, format_source_code


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.get("/")
def index():
    return render_template("index.html", asset_version=str(int(time.time())))


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.post("/api/compile")
def api_compile():
    payload = request.get_json(silent=True) or {}
    source_code = payload.get("source", "")
    source_code = "" if source_code is None else str(source_code)
    trace_mode = bool(payload.get("trace", False))

    if not source_code.strip():
        return jsonify({"success": False, "errors": ["No source code provided."]}), 400

    result = compile_source(source_code, trace=trace_mode)
    return jsonify(result)


@app.post("/api/format")
def api_format():
    payload = request.get_json(silent=True) or {}
    source_code = payload.get("source", "")
    source_code = "" if source_code is None else str(source_code)

    if not source_code.strip():
        return jsonify({"success": False, "errors": ["No source code provided."]}), 400

    formatted = format_source_code(source_code)
    return jsonify({"success": True, "formatted": formatted})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
