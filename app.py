from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import subprocess
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# ✅ Health check route
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend is running"}), 200

# ✅ Main protect PDF route
@app.route('/protect-pdf', methods=['POST'])
def protect_pdf():
    print("Received protect-pdf request")  # For Render logs

    if 'pdf' not in request.files or 'password' not in request.form:
        return jsonify({"error": "PDF file and password are required"}), 400

    pdf_file = request.files['pdf']
    password = request.form['password']

    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.pdf")
            decrypted_path = os.path.join(tmpdir, "decrypted.pdf")
            output_path = os.path.join(tmpdir, "protected.pdf")

            # Save uploaded file
            pdf_file.save(input_path)

            # ✅ Step 1: Try to decrypt (in case it's already encrypted)
            try:
                subprocess.run(
                    ["qpdf", "--decrypt", input_path, decrypted_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                input_for_encryption = decrypted_path
            except subprocess.CalledProcessError:
                # If decrypt fails, assume it's not encrypted and use original
                input_for_encryption = input_path

            # ✅ Step 2: Encrypt the (possibly decrypted) PDF
            encrypt_command = [
                "qpdf", "--encrypt", password, password, "256", "--",
                input_for_encryption, output_path
            ]
            result = subprocess.run(
                encrypt_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            # ✅ Return protected file
            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"protected_{pdf_file.filename}",
                mimetype='application/pdf'
            )

    except subprocess.CalledProcessError as e:
        print("QPDF Error:", e.stderr.decode())  # Log actual qpdf error
        return jsonify({"error": "Failed to protect PDF: " + e.stderr.decode()}), 500

    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ Render/local port binding
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default for local dev
    app.run(host='0.0.0.0', port=port)
