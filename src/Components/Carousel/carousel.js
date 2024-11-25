import React, { useState, useEffect } from 'react';
import Slider from 'react-slick';
import foodItemsData from '../../Foodservices.Fooditems.json';
import './carousel.css';

function CuisineCarousel({ cuisine }) {
  const [items] = useState(foodItemsData);
  const [cartItems, setCartItems] = useState([]);

  // Filter items to only show those that match the cuisine prop
  const filteredItems = items.filter(item => item.cuisine === cuisine);

  // Load cart items from session storage on component mount
  useEffect(() => {
    const storedCartItems = JSON.parse(sessionStorage.getItem("cart")) || [];
    setCartItems(storedCartItems);
  }, []);

  // Function to update session storage and state when cart items change
  const updateCart = (updatedCartItems) => {
    setCartItems(updatedCartItems);
    sessionStorage.setItem("cart", JSON.stringify(updatedCartItems));
  };

  // Function to add items to cart
  const addToCart = (item) => {
    const updatedCartItems = [...cartItems];
    const existingItemIndex = updatedCartItems.findIndex(cartItem => cartItem.foodId === item.foodId);

    if (existingItemIndex !== -1) {
      updatedCartItems[existingItemIndex].quantity += 1;
    } else {
      updatedCartItems.push({ ...item, image: item.imageUrl, quantity: 1 }); // Ensure image is correctly mapped
    }

    updateCart(updatedCartItems);
  };

  // Function to reduce quantity of items in the cart
  const reduceQuantity = (item) => {
    const updatedCartItems = cartItems.map(cartItem => {
      if (cartItem.foodId === item.foodId) {
        return { ...cartItem, quantity: cartItem.quantity - 1 };
      }
      return cartItem;
    }).filter(cartItem => cartItem.quantity > 0);

    updateCart(updatedCartItems);
  };

  const settings = {
    autoplay: true,
    autoplaySpeed: 2000,
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: true,
    responsive: [
      {
        breakpoint: 1024,
        settings: { slidesToShow: 3 },
      },
      {
        breakpoint: 768,
        settings: { slidesToShow: 2 },
      },
      {
        breakpoint: 480,
        settings: { slidesToShow: 1 },
      },
    ],
  };

  return (
    <div className='cc-carousel'>
      <Slider {...settings} className="cuisine-carousel">
        {filteredItems.map((item, index) => {
          const cartItem = cartItems.find(cartItem => cartItem.foodId === item.foodId);
          const quantity = cartItem ? cartItem.quantity : 0;

          return (
            <div key={index} className="cuisine-item">
              <img src={item.imageUrl} alt={item.name} />
              <p>{item.name}</p>
              <p>{`$${item.price.toFixed(2)}`}</p>
              <p className='item-description'>{item.description}</p>
              {quantity > 0 ? (
                <div className="quantity-incrementer">
                  <button onClick={() => reduceQuantity(item)}>-</button>
                  <span>{quantity}</span>
                  <button onClick={() => addToCart(item)}>+</button>
                </div>
              ) : (
                <button className="add-to-cart-button" onClick={() => addToCart(item)}>
                  Add to Cart
                </button>
              )}
            </div>
          );
        })}
      </Slider>
    </div>
  );
}

export default CuisineCarousel;
