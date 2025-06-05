import React, { useState } from 'react';

export default function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    setIsUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('playlist', file);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });      

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
      } else {
        setMessage(data.error || 'Upload failed');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('Connection error');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h2>Sync Playlist to Spotify</h2>

      <input type="file" accept=".xml" onChange={handleFileChange} />

      <button
        onClick={handleUpload}
        disabled={!file || isUploading}
        style={{
          padding: '10px 20px',
          backgroundColor: isUploading ? '#ccc' : '#1db954',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: isUploading ? 'not-allowed' : 'pointer',
          marginTop: '10px'
        }}
      >
        {isUploading ? 'Syncing...' : 'Sync'}
      </button>

      {message && (
        <p
          style={{
            color: message.toLowerCase().includes('success') ? 'green' : 'red',
            fontWeight: 'bold',
            marginTop: '10px'
          }}
        >
          {message}
        </p>
      )}

      {file && (
        <p style={{ color: '#666', fontSize: '14px', marginTop: '5px' }}>
          Selected file: {file.name}
        </p>
      )}
    </div>
  );
}
