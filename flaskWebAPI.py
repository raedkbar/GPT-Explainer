import glob
import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOADS_DIR = "uploads"
OUTPUTS_DIR = "outputs"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Generate UID for the file
    uid = str(uuid.uuid4())

    # Create timestamp for the upload
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the filename with original filename, timestamp, and UID
    filename = secure_filename(file.filename)
    new_filename = f"{filename}_{timestamp}_{uid}"

    # Save the file to the uploads folder
    file.save(os.path.join(UPLOADS_DIR, new_filename))

    return jsonify({"uid": uid}), 200


@app.route("/status/<uid>", methods=["GET"])
def get_status(uid):
    # Check if the upload exists
    upload_path = os.path.join(UPLOADS_DIR, f"*_{uid}")
    matching_uploads = glob.glob(upload_path)

    if len(matching_uploads) == 0:
        return jsonify({"status": "not found"}), 404

    upload_filename = os.path.basename(matching_uploads[0])
    timestamp = upload_filename.split("_")[1]

    output_path = os.path.join(OUTPUTS_DIR, f"{upload_filename}.json")

    # Check if the output file exists
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            output_data = json.load(f)

        return jsonify({
            "status": "done",
            "filename": upload_filename,
            "timestamp": timestamp,
            "explanation": output_data
        })

    return jsonify({
        "status": "pending",
        "filename": upload_filename,
        "timestamp": timestamp,
        "explanation": None
    })


if __name__ == "__main__":
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    app.run()
