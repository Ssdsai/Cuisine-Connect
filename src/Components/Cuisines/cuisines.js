import React from 'react';
import CuisineCarousel from '../Carousel/carousel';
import './cuisines.css';

const cuisines = [
  { name: 'Italian' },
  { name: 'Indian' },
  { name: 'Mexican' },
  { name: 'Thai' },
  { name: 'Korean' },
  { name: 'Japanese' },
  { name: 'American' },
  { name: 'Chinese' },
];

function Cuisines() {
  return (
    <div className="cuisines-section" id="cuisines">
      {cuisines.map((cuisine, index) => (
        <div key={index} className="cuisine-box">
          <h3>{cuisine.name}</h3>
          <CuisineCarousel cuisine={cuisine.name} /> {/* Pass cuisine name as prop */}
        </div>
      ))}
    </div>
  );
}

export default Cuisines;
