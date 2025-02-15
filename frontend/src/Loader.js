import React from 'react';
import './App.css'; // Ensure this file contains the loader CSS

const Loader = () => {
  return (
    <div className="loader-container">
      <div className="loader">
        <div className="crystal"></div>
        <div className="crystal"></div>
        <div className="crystal"></div>
        <div className="crystal"></div>
        <div className="crystal"></div>
        <div className="crystal"></div>
      </div>
    </div>
  );
};

export default Loader;