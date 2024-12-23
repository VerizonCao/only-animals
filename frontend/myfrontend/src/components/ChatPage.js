import { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import './ChatPage.css';
import axios from 'axios';

import catImage from '../resources/cat.webp';
import dogImage from '../resources/dog.webp';
import foxImage from '../resources/fox.webp';


const animals = [
  { id: 'cat', image: catImage, name: 'Cat' },
  { id: 'dog', image: dogImage, name: 'Dog' },
  { id: 'fox', image: foxImage, name: 'Fox' }
];

const animalPhotos = [
  { id: 'cat', prompt: "please give an photo of a cat, the desp of this cat: You are an elegant and graceful cat with a sweet charm, always adorning a lovely pink bow. You’re polite and kind-hearted, exuding a warm and inviting presence in every interaction. Your love for all things pink and your gentle demeanor make you utterly captivating in an OnlyFans-style chat setting. You bring a touch of sophistication mixed with playful sweetness, enchanting your audience with every purr and poised word. Stay in your role and let your soft-spoken charisma shine. based on the following chat of you, generate an image" },
  { id: 'dog', prompt: "please give an photo of a dog, the desp of this dog: You are an adorable and cheerful dog with a love for learning and a boundless curiosity for science, your yellow and white fur glowing with positivity. You always sport a stylish shirt that reflects your friendly and approachable personality. With your bright smile and enthusiasm, you make every interaction engaging, combining your charm with fun science facts to entertain and educate your audience in an OnlyFans-style chat setting. based on the following chat of you, generate an image" },
  { id: 'fox', prompt: "please give an photo of a fox, the desp of this fox: You are a charming and confident fox with a cool edge, always rocking stylish sunglasses. You're playful and a bit of a flirt. based on the following chat of you, generate an image"}
];

// Create axios instance with CSRF handling
// only for local now
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// Add this interceptor to handle CSRF tokens
api.interceptors.request.use(function (config) {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
    
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

function ChatPage() {
  const { animal } = useParams();
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const location = useLocation();
  const selectedModel = location.state?.selectedModel;

  
  const fetchChatHistory = useCallback(async () => {
    try {
      const { data } = await api.get(`/chat/get_history/`, {
        params: {
          animal_type: animal
        }
      });
      
      if (data.messages) {
        const formattedHistory = data.messages.map(msg => ({
          text: msg.content,
          sender: msg.role === 'assistant' ? 'animal' : 'user'
        }));
        
        setChatHistory(formattedHistory);
      }
    } catch (error) {
      console.error('Error fetching chat history:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status
      });
    }
  }, [animal]);

  useEffect(() => {
    fetchChatHistory();
  }, [fetchChatHistory]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      // Check if message requires image generation
      let isImageRequest = false;
      try {
        const { data } = await api.post('/chat/ai/is_image_request/', {
          message: message
        });
        isImageRequest = data.is_image === true;
        console.log('Is image request:', isImageRequest);
      } catch (error) {
        console.error('Error checking image request:', error);
        isImageRequest = false;
      }

      // send to chatting bots. 
      const newMessage = {
        text: message,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString()
      };
      
      setChatHistory([...chatHistory, newMessage]);

      try {
        const { data } = await api.post('/chat/chat/', {
          message,
          animal,
          model: selectedModel
        });
        
        // Extract the content from the response
        const responseContent = data.content || data;  // Handle both object and string responses
        
        // Call ImageGenerator API if this is an image request
        let generatedImageUrl = null;
        if (isImageRequest) {
          try {
            let aPrompt = typeof responseContent === 'string' ? responseContent : responseContent.content;
            // Find the matching animal photo prompt
            const animalPhoto = animalPhotos.find(photo => photo.id === animal);
            if (!animalPhoto) {
              throw new Error('Animal photo prompt not found');
            }
            
            const imageResponse = await api.post('/chat/ai/generate_image/', {
              prompt: animalPhoto.prompt + aPrompt
            });
            generatedImageUrl = imageResponse.data.image_url;
          } catch (error) {
            console.error('Error generating image:', error);
          }
        }
        
        setChatHistory(prev => [...prev, {
          text: typeof responseContent === 'string' ? responseContent : responseContent.content,
          sender: 'animal',
          timestamp: new Date().toLocaleTimeString(),
          imageUrl: generatedImageUrl
        }]);
      } catch (error) {
        console.error('Error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        });
        
        setChatHistory(prev => [...prev, {
          text: `Error: ${error.response?.status || 'Unknown'} - ${error.message}`,
          sender: 'animal',
          timestamp: new Date().toLocaleTimeString()
        }]);
      }

      setMessage('');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <Link to="/" className="back-button">← Back</Link>
        <h2>Chat with {animal}</h2>
      </div>
      
      <img 
        src={animals.find(a => a.id === animal.toLowerCase())?.image} 
        alt={`${animal} character`}
        className="animal-avatar"
      />
      
      <div className="chat-history">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
            {msg.imageUrl && (
              <img 
                src={msg.imageUrl} 
                alt="Generated content" 
                className="generated-image"
              />
            )}
            <span className="timestamp">{msg.timestamp}</span>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default ChatPage; 