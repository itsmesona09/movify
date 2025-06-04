from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from main import migrate_playlist  # your existing function
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    if 'playlist' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['playlist']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xml') as temp_file:
        file.save(temp_file.name)
        try:
            base = os.path.basename(temp_file.name)
            migrate_playlist(temp_file.name, os.path.splitext(base)[0])
            return jsonify({'message': 'Playlist synced successfully!'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
