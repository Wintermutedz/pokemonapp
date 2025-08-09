import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

function App() {
  const [cards, setCards] = useState([]);
  const [uploading, setUploading] = useState(false);

  const onDrop = async (acceptedFiles) => {
    setUploading(true);
    const formData = new FormData();
    acceptedFiles.forEach(file => formData.append('files', file));
    try {
      const response = await axios.post('http://localhost:8899/upload', formData);
      setCards(response.data.cards);
    } catch (err) {
      alert('Error identifying cards.');
    }
    setUploading(false);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const addToCollection = async (cardId) => {
    await axios.post('http://localhost:8899/collection', { id: cardId });
    alert('Card added to collection!');
  };

  return (
    <div className="app-container">
      <h1>Pokémon Card Identifier</h1>
      <div {...getRootProps()} style={{
        border: '2px dashed #aaa',
        padding: '2rem',
        textAlign: 'center',
        marginBottom: '2rem',
        background: '#fafafa'
      }}>
        <input {...getInputProps()} />
        {uploading ? <p>Uploading...</p> : <p>Drag and drop card images here</p>}
      </div>
      <div className="card-grid">
        {cards.map(card => (
          <div className="card" key={card.id}>
            <img src={card.image} alt={card.name} />
            <h3>{card.name}</h3>
            <p>{card.rarity} — {card.set}</p>
            <p>🪙 ${card.price} ({card.history.join(', ')})</p>
            <button onClick={() => addToCollection(card.id)}>Add to Collection</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;