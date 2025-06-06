from flask import Flask, request, jsonify
from flask_cors import CORS
from main import migrate_playlist
import os, tempfile

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
            base = os.path.basename(file.filename)
            name = os.path.splitext(base)[0]
            migrate_playlist(temp_file.name, name)
            return jsonify({'message': 'Playlist synced successfully!'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
