// App.jsx
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus('');
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('❌ No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('playlist', file);

    try {
      setStatus('🔄 Syncing playlist...');
      const res = await axios.post('http://localhost:5000/upload', formData);
      setStatus(`✅ ${res.data.message}`);
    } catch (err) {
      setStatus(`❌ Failed to sync: ${err.response?.data?.error || err.message}`);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">🎵 Spotify Playlist Sync</h1>
      <input type="file" accept=".xml" onChange={handleFileChange} className="mb-4" />
      <br />
      <button onClick={handleUpload} className="bg-green-600 text-white px-4 py-2 rounded">
        🔁 Sync with Spotify
      </button>
      <p className="mt-4">{status}</p>
    </div>
  );
}

export default App;
