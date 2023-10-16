import os
import json
import uuid

from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename
from pkg.db_util.db_session import create_session
from pkg.db_util.ORM import Upload, User

app = Flask(__name__)
UPLOADS_DIR = "../uploads"
OUTPUTS_DIR = "../outputs"

# Create the upload and output directories if they don't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

session = create_session()


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Uploads a file to the server.

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
    timestamp = datetime.now()

    # Create the filename with original filename, timestamp, and UID
    filename = secure_filename(file.filename)

    # Save the file to the uploads folder
    file.save(os.path.join(UPLOADS_DIR, f"{uid}.pptx"))

    email = request.form.get("email")
    user = None

    if email:
        # Query the User table for the user with the specified email
        user = session.query(User).filter_by(email=email).first()
        if not user:
            # User not found, create a new user
            user = User(email=email)
            session.add(user)
            session.commit()

    # Create an Upload object and commit it to the database
    upload = Upload(uid=uid, filename=filename, upload_time=timestamp, status="pending", user=user)
    session.add(upload)
    session.commit()

    return jsonify({"uid": uid}), 200


@app.route("/status", methods=["GET"])
def get_status():
    """
    Retrieves the status of an upload.

    Returns:
        JSON response with the status, filename, timestamp, and explanation
    """
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    email = request.args.get('email')
    upload = None

    if uid:
        upload = session.query(Upload).filter_by(uid=uid).first()
    elif filename and email:
        user = session.query(User).filter_by(email=email).first()
        upload = (
            session.query(Upload)
            .filter_by(filename=filename, user=user)
            .order_by(Upload.upload_time.desc())
            .first()
        )

    if not upload:
        return jsonify({'error': 'Upload not found'}), 404

    # Retrieve the status, filename, and timestamp
    status = upload.status
    filename = upload.filename
    timestamp = upload.upload_time

    # Check if the upload has finished processing
    explanation = ""
    if status == "completed":
        explanation_file = os.path.join(OUTPUTS_DIR, f"{uid}.json")
        if os.path.exists(explanation_file):
            with open(explanation_file, "r") as f:
                explanation_data = json.load(f)
            explanation = '\n'.join(slide['explanation'] for slide in explanation_data)
    elif status == "failed":
        explanation = "Processing failed"
    else:
        explanation = "Processing in progress"

    return jsonify({
        "status": status,
        "filename": filename,
        "timestamp": timestamp,
        "explanation": explanation
    }), 200


if __name__ == "__main__":
    app.run()
