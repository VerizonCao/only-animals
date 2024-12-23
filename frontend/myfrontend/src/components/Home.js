import { useNavigate } from 'react-router-dom';
import './Home.css';
import catImage from '../resources/cat.webp';
import dogImage from '../resources/dog.webp';
import foxImage from '../resources/fox.webp';
import { useState } from 'react';

function Home() {
  const navigate = useNavigate();
  const animals = [
    { id: 'cat', image: catImage, name: 'Cat' },
    { id: 'dog', image: dogImage, name: 'Dog' },
    { id: 'fox', image: foxImage, name: 'Fox' }
  ];

  const [selectedModel, setSelectedModel] = useState(() => {
    return localStorage.getItem('selectedModel') || "meta-llama/Llama-3.2-3B-Instruct"
  });

  const modelToggle = (
    <div className="model-selector">
      <label className="model-toggle">
        <span>Select Model: </span>
        <select 
          value={selectedModel} 
          onChange={(e) => {
            console.log('Changing model to:', e.target.value);
            setSelectedModel(e.target.value);
            localStorage.setItem('selectedModel', e.target.value);
          }}
          className="model-select"
        >
          <option value="meta-llama/Llama-3.2-3B-Instruct">Llama-3.2-3B</option>
          <option value="mistralai/Mistral-7B-Instruct-v0.3">Mistral-7B</option>
        </select>
      </label>
    </div>
  );

  const handleAnimalClick = (animalId) => {
    console.log('Navigating with model:', selectedModel);
    navigate(`/chat/${animalId}`, { state: { selectedModel } });
  };

  return (
    <div className="home-container">
      <h1>OnlyAnimals</h1>
      <div className="animals-grid">
        {modelToggle}
        {animals.map((animal) => (
          <div 
            key={animal.id} 
            className="animal-card"
            onClick={() => handleAnimalClick(animal.id)}
          >
            <img src={animal.image} alt={animal.name} />
            <h2>{animal.name}</h2>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home; 