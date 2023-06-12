import glob
import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

app = Flask(__name__)
UPLOADS_DIR = "./uploads"
OUTPUTS_DIR = "./outputs"

# Create the upload and output directories if they don't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Uploads a file to the server.

    Args:
        None (request is accessed directly)

    Returns:
        JSON response with UID if successful, error message otherwise
    """
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
    name, extension = filename.rsplit('.', 1)
    new_filename = f"{name}_{timestamp}_{uid}.{extension}"

    # Save the file to the uploads folder
    file.save(os.path.join(UPLOADS_DIR, new_filename))

    return jsonify({"uid": uid}), 200


@app.route("/status/<uid>", methods=["GET"])
def get_status(uid):
    """
    Retrieves the status of an upload.

    Args:
        uid (str): The unique identifier for the upload

    Returns:
        JSON response with the status, filename, timestamp, and explanation
    """
    # Check if the upload exists
    upload_path = os.path.join(UPLOADS_DIR, f"*_{uid}.*")
    matching_uploads = glob.glob(upload_path)

    if len(matching_uploads) == 0:
        return jsonify({"status": "not found"}), 404

    upload_filename = os.path.basename(matching_uploads[0])
    timestamp = upload_filename.split("_")[-2]

    stripped_string = upload_filename.split("_", 1)[1]

    output_path = Path(OUTPUTS_DIR) / f"{stripped_string.split('.')[0]}.json"
    output_path = output_path.resolve()

    # Check if the output file exists
    if output_path.exists():
        with open(output_path, "r") as f:
            output_data = json.load(f)

        # Extract all slides explanation
        explanation = ''.join(slide["explanation"] for slide in output_data)

        return jsonify({
            "status": "done",
            "filename": upload_filename,
            "timestamp": timestamp,
            "explanation": explanation
        })

    return jsonify({
        "status": "pending",
        "filename": upload_filename,
        "timestamp": timestamp,
        "explanation": None
    })


if __name__ == "__main__":
    app.run()
