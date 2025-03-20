// stripe_kong/static/stripe_kong/js/puck/src/renderer.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import PuckEditor from './PuckEditor';

// Global function to initialize the renderer
window.renderPuckPage = (containerId, pageData) => {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error(`Container element #${containerId} not found`);
    return;
  }

  const root = createRoot(container);
  
  root.render(
    <PuckEditor 
      initialData={pageData} 
      readOnly={true} 
    />
  );
};
