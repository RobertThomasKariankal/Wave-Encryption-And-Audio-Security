from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "encrypted"
DECRYPTED_FOLDER = "decrypted"
KEY_FOLDER = "keys"

# Ensure necessary directories exist
for folder in [UPLOAD_FOLDER, ENCRYPTED_FOLDER, DECRYPTED_FOLDER, KEY_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Generate encryption key
    key = Fernet.generate_key()
    key_filename = "key.key"
    key_path = os.path.join(KEY_FOLDER, key_filename)

    with open(key_path, "wb") as key_file:
        key_file.write(key)

    # Encrypt file
    fernet = Fernet(key)
    with open(filepath, "rb") as f:
        encrypted_data = fernet.encrypt(f.read())

    encrypted_filename = f"encrypted_{file.filename}"
    encrypted_path = os.path.join(ENCRYPTED_FOLDER, encrypted_filename)

    with open(encrypted_path, "wb") as enc_file:
        enc_file.write(encrypted_data)

    return jsonify({
        "encrypted_url": f"/download/encrypted/{encrypted_filename}",
        "key_url": f"/download/keys/{key_filename}"
    })

@app.route("/decrypt", methods=["POST"])
def decrypt():
    file = request.files["file"]
    key_file = request.files["key"]

    encrypted_filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    key_filepath = os.path.join(KEY_FOLDER, key_file.filename)

    file.save(encrypted_filepath)
    key_file.save(key_filepath)

    # Load encryption key
    with open(key_filepath, "rb") as kf:
        key = kf.read()

    fernet = Fernet(key)
    with open(encrypted_filepath, "rb") as enc_file:
        decrypted_data = fernet.decrypt(enc_file.read())

    decrypted_filename = f"decrypted_{file.filename}"
    decrypted_path = os.path.join(DECRYPTED_FOLDER, decrypted_filename)

    with open(decrypted_path, "wb") as dec_file:
        dec_file.write(decrypted_data)

    return jsonify({"decrypted_url": f"/download/decrypted/{decrypted_filename}"})

@app.route("/download/<folder>/<filename>")
def download(folder, filename):
    """Serve files from the correct folders."""
    if folder == "encrypted":
        return send_from_directory(ENCRYPTED_FOLDER, filename, as_attachment=True)
    elif folder == "keys":
        return send_from_directory(KEY_FOLDER, filename, as_attachment=True)
    elif folder == "decrypted":
        return send_from_directory(DECRYPTED_FOLDER, filename, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
