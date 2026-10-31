#!/usr/bin/env python3
"""
Glassy Print Hub - Web Interface for Brother DCP-T236 Print Server
Runs on Raspberry Pi 4 (via CUPS) and supports Windows development / simulation.
"""

import os
import sys
import time
import uuid
import shutil
import platform
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
from PIL import Image

try:
    import pypdfium2 as pdfium
    HAS_PDFIUM = True
except ImportError:
    HAS_PDFIUM = False

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
THUMBNAIL_FOLDER = BASE_DIR / "uploads" / "thumbnails"
UPLOAD_FOLDER.mkdir(exist_ok=True)
THUMBNAIL_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64 MB max upload

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "txt", "docx"}

# In-memory job tracker for real-time tracking
JOBS = []

def is_linux():
    return platform.system() == "Linux"

def get_cups_printers():
    """Detect printers using lpstat on Linux."""
    if not is_linux():
        return [{"name": "Brother_DCP-T236 (Simulated)", "status": "Ready", "is_default": True}]
    
    try:
        res = subprocess.run(["lpstat", "-p", "-d"], capture_output=True, text=True, timeout=5)
        lines = res.stdout.splitlines()
        printers = []
        default_printer = None
        for line in lines:
            if "system default destination:" in line:
                default_printer = line.split(":")[-1].strip()
            elif line.startswith("printer "):
                parts = line.split()
                if len(parts) >= 2:
                    pname = parts[1]
                    status = "Idle"
                    if "is idle" in line:
                        status = "Idle / Ready"
                    elif "printing" in line:
                        status = "Printing..."
                    elif "disabled" in line:
                        status = "Paused"
                    printers.append({
                        "name": pname,
                        "status": status,
                        "is_default": (pname == default_printer)
                    })
        if not printers:
            # Fallback if cups daemon is installed but no queue added yet
            return [{"name": "Brother_DCP-T236", "status": "Ready (Default Queue)", "is_default": True}]
        return printers
    except Exception as e:
        return [{"name": "Brother_DCP-T236", "status": f"CUPS Query Error ({e})", "is_default": True}]

def get_active_jobs_from_cups():
    """Query CUPS for pending/processing jobs."""
    if not is_linux():
        # Update simulation progress
        now = time.time()
        for j in JOBS:
            if j["status"] == "Printing":
                if now - j["start_time"] > 6:
                    j["status"] = "Completed"
                    j["progress"] = 100
                else:
                    j["progress"] = min(95, int(((now - j["start_time"]) / 6.0) * 100))
        return JOBS
    
    try:
        res = subprocess.run(["lpstat", "-o"], capture_output=True, text=True, timeout=5)
        active_lines = res.stdout.strip().splitlines()
        active_job_ids = [line.split()[0] for line in active_lines if line]
        
        for j in JOBS:
            if j.get("cups_job_id") in active_job_ids:
                j["status"] = "Printing"
            elif j["status"] == "Printing":
                j["status"] = "Completed"
                j["progress"] = 100
        return JOBS
    except Exception:
        return JOBS

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_thumbnail(filepath, filename):
    """Generate image preview for PDF or image uploads."""
    ext = filepath.suffix.lower()
    thumb_path = THUMBNAIL_FOLDER / f"{filename}.png"
    
    if thumb_path.exists():
        return f"/uploads/thumbnails/{filename}.png"

    try:
        if ext in [".png", ".jpg", ".jpeg"]:
            with Image.open(filepath) as img:
                img.thumbnail((500, 700))
                img.save(thumb_path, "PNG")
                return f"/uploads/thumbnails/{filename}.png"
                
        elif ext == ".pdf" and HAS_PDFIUM:
            pdf = pdfium.PdfDocument(filepath)
            if len(pdf) > 0:
                first_page = pdf[0]
                pil_image = first_page.render(scale=2).to_pil()
                pil_image.thumbnail((500, 700))
                pil_image.save(thumb_path, "PNG")
                return f"/uploads/thumbnails/{filename}.png"
    except Exception as err:
        print(f"[-] Thumbnail generation error: {err}")
    
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    printers = get_cups_printers()
    jobs = get_active_jobs_from_cups()
    return jsonify({
        "platform": platform.system(),
        "is_linux": is_linux(),
        "printers": printers,
        "active_jobs_count": sum(1 for j in jobs if j["status"] in ["Queued", "Printing"]),
        "server_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/api/upload-preview", methods=["POST"])
def upload_preview():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
    
    unique_prefix = uuid.uuid4().hex[:8]
    clean_name = secure_filename(file.filename)
    saved_name = f"{unique_prefix}_{clean_name}"
    dest_path = UPLOAD_FOLDER / saved_name
    file.save(dest_path)
    
    preview_url = generate_thumbnail(dest_path, saved_name)
    file_size_kb = round(os.path.getsize(dest_path) / 1024, 1)

    return jsonify({
        "success": True,
        "saved_filename": saved_name,
        "original_name": file.filename,
        "size_kb": file_size_kb,
        "preview_url": preview_url,
        "file_url": f"/uploads/{saved_name}"
    })

@app.route("/api/print", methods=["POST"])
def print_document():
    data = request.json or {}
    saved_filename = data.get("filename")
    if not saved_filename:
        return jsonify({"error": "No file specified"}), 400
    
    file_path = UPLOAD_FOLDER / secure_filename(saved_filename)
    if not file_path.exists():
        return jsonify({"error": "File not found on server"}), 404

    # Options
    printer_name = data.get("printer_name", "Brother_DCP-T236")
    color_mode = data.get("color_mode", "color")  # "color" or "monochrome"
    copies = int(data.get("copies", 1))
    media_size = data.get("media_size", "A4")     # "A4", "Letter", "4x6"
    orientation = data.get("orientation", "portrait") # "portrait" or "landscape"
    page_range = data.get("page_range", "").strip()

    job_id = f"JOB-{int(time.time())}-{uuid.uuid4().hex[:4].upper()}"
    cups_job_id = None
    exec_cmd = []

    if is_linux():
        # Build CUPS `lp` command
        cmd = ["lp"]
        if printer_name and not "Simulated" in printer_name:
            cmd.extend(["-d", printer_name])
        cmd.extend(["-n", str(copies)])
        cmd.extend(["-o", f"media={media_size}"])
        
        # Color option
        if color_mode == "monochrome":
            cmd.extend(["-o", "ColorModel=Gray", "-o", "print-color-mode=monochrome"])
        else:
            cmd.extend(["-o", "ColorModel=Color", "-o", "print-color-mode=color"])
            
        # Orientation (3 = Portrait, 4 = Landscape)
        if orientation == "landscape":
            cmd.extend(["-o", "orientation-requested=4"])
        else:
            cmd.extend(["-o", "orientation-requested=3"])

        if page_range:
            cmd.extend(["-P", page_range])

        cmd.append(str(file_path))
        exec_cmd = cmd

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Output is usually: "request id is Brother_DCP-T236-42 (1 file(s))"
            out = res.stdout.strip()
            if "request id is " in out:
                cups_job_id = out.split("request id is ")[1].split()[0]
        except Exception as e:
            return jsonify({"error": f"Failed to submit print job to CUPS: {e}"}), 500
    else:
        # Simulated Windows / Development command
        exec_cmd = [
            "lp", "-d", printer_name, "-n", str(copies),
            "-o", f"media={media_size}",
            "-o", f"ColorModel={'Gray' if color_mode == 'monochrome' else 'Color'}",
            str(file_path.name)
        ]

    job_record = {
        "id": job_id,
        "cups_job_id": cups_job_id,
        "filename": saved_filename,
        "display_name": data.get("display_name", saved_filename),
        "printer": printer_name,
        "color_mode": color_mode,
        "copies": copies,
        "media_size": media_size,
        "orientation": orientation,
        "status": "Printing",
        "progress": 20,
        "start_time": time.time(),
        "submitted_at": time.strftime("%H:%M:%S"),
        "command_preview": " ".join(exec_cmd)
    }
    JOBS.insert(0, job_record)

    return jsonify({
        "success": True,
        "message": f"Print job {job_id} dispatched successfully!",
        "job": job_record
    })

@app.route("/api/jobs")
def get_jobs():
    jobs = get_active_jobs_from_cups()
    return jsonify({"jobs": jobs[:20]})

@app.route("/api/jobs/<job_id>/cancel", methods=["POST"])
def cancel_job(job_id):
    for j in JOBS:
        if j["id"] == job_id:
            if is_linux() and j.get("cups_job_id"):
                try:
                    subprocess.run(["cancel", j["cups_job_id"]], check=True)
                except Exception:
                    pass
            j["status"] = "Cancelled"
            j["progress"] = 0
            return jsonify({"success": True, "message": f"Job {job_id} cancelled"})
    return jsonify({"error": "Job not found"}), 404

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(str(UPLOAD_FOLDER), filename)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    print("=" * 65)
    print(" 🚀 GLASSY PRINT HUB SERVER RUNNING")
    print("=" * 65)
    print(f" Local Access:   http://localhost:{port}")
    print(f" Network Access: http://<your-pi-ip>:{port} or http://printserver.local:{port}")
    print(" Press Ctrl+C to terminate.")
    print("=" * 65)
    app.run(host=host, port=port, debug=True)
