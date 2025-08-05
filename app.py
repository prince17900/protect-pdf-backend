from flask import Flask, request, send_file, jsonify
import os
import subprocess
import tempfile
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend is running"}), 200

@app.route('/protect-pdf', methods=['POST'])
def protect_pdf():
    print("Received protect-pdf request")  # 👈 Add this
    ...


@app.route('/protect-pdf', methods=['POST'])
def protect_pdf():
    if 'pdf' not in request.files or 'password' not in request.form:
        return jsonify({"error": "PDF file and password are required"}), 400

    pdf_file = request.files['pdf']
    password = request.form['password']

    if pdf_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.pdf")
            output_path = os.path.join(tmpdir, "protected.pdf")

            # Save the uploaded PDF
            pdf_file.save(input_path)

            # Encrypt PDF using qpdf
            command = [
                "qpdf",
                "--encrypt", password, password, "256",
                "--", input_path, output_path
            ]
            subprocess.run(command, check=True)

            # Send the protected PDF back
            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"protected_{pdf_file.filename}",
                mimetype='application/pdf'
            )

    except subprocess.CalledProcessError:
        return jsonify({"error": "Failed to protect PDF. qpdf error."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

    

