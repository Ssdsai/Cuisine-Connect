import React from "react";
import Navbar from './Navbar/navbar'
import Slider from './Slider/slider'
import Cuisines from './Cuisines/cuisines'
import { useNavigate } from 'react-router-dom';
import './iconbot.css'; // Custom styles for positioning and icon design
import Footer from "./Foooter/footer";

const Home = () => {
  const navigate = useNavigate();
  return (
    
      <div className="product-sections">
        <Navbar />
        <Slider />
        <Cuisines />
        <div className="chatbot-icon" onClick={() => navigate('/chatbot')}>
          <img src="/images/chat.jpg" alt="Chatbot Icon" />
        </div>
        <Footer />
        <div className="products-container">
          
          
        </div>
      </div>
  );
}

export default Home;



