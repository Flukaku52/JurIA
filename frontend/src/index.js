import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Criando a raiz do React
const root = ReactDOM.createRoot(document.getElementById('root'));

// Renderizando o componente App
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 