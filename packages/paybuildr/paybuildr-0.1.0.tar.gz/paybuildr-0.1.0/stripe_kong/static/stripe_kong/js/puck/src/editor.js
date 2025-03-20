// stripe_kong/static/stripe_kong/js/puck/src/editor.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import PuckEditor from './PuckEditor';

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Global function to initialize the editor
window.initPuckEditor = (containerId, initialData, saveUrl) => {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Container element #${containerId} not found`);
    return;
  }

  const root = createRoot(container);

  const handleSave = async (data) => {
    try {
      const response = await fetch(saveUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`Failed to save: ${response.statusText}`);
      }

      const result = await response.json();
      if (result.success) {
        alert('Page saved successfully!');
      } else {
        throw new Error('Failed to save page');
      }
    } catch (error) {
      console.error('Error saving page:', error);
      alert(`Error saving page: ${error.message}`);
    }
  };

  root.render(
    <PuckEditor 
      initialData={initialData} 
      onSave={handleSave} 
    />
  );
};
