from __future__ import annotations
import os
from flask import render_template, send_from_directory
from . import create_app
from .extensions import socketio

app = create_app()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/login")
def login_page():
    return render_template("auth.html")


@app.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.get("/rooms-ui")
def rooms_ui():
    return render_template("rooms.html")


@app.get("/gigs-ui")
def gigs_ui():
    return render_template("gigs.html")


@app.get("/profile")
def profile_ui():
    return render_template("profile.html")


@app.route('/pwa/<path:filename>')
def pwa_files(filename):
    pwa_dir = os.path.join(app.root_path, 'pwa')
    return send_from_directory(pwa_dir, filename)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000)
