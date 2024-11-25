import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Cart/cart.css';
import Navbar from '../Navbar/navbar';
import Footer from '../Foooter/footer';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in, else redirect to login
    if (localStorage.getItem("isLoggedIn") !== "true") {
      navigate("/login");
      return;
    }

    // Fetch cart items from session storage
    const storedCartItems = JSON.parse(sessionStorage.getItem("cart")) || [];
    setCartItems(storedCartItems);
  }, [navigate]);

  const handleQuantityChange = (index, newQuantity) => {
    const updatedCartItems = [...cartItems];
    updatedCartItems[index].quantity = Math.max(1, parseInt(newQuantity, 10)); // Ensure it doesn't go below 1
    setCartItems(updatedCartItems);
    sessionStorage.setItem("cart", JSON.stringify(updatedCartItems));
  };

  const handleRemoveItem = (index) => {
    const updatedCartItems = cartItems.filter((_, i) => i !== index);
    setCartItems(updatedCartItems);
    sessionStorage.setItem("cart", JSON.stringify(updatedCartItems));
  };

  const totalPrice = cartItems.reduce((acc, item) => {
    const price = typeof item.price === 'number' ? item.price : 0; // Fallback to 0 if price is undefined
    return acc + (price * (item.quantity || 0)); // Safely handle undefined quantity
  }, 0);

  return (
    <div className="cart-page">
      <Navbar />
      <h1 className="cart-heading">Your Cart</h1>
      <div className="cart-items">
      {cartItems.length === 0 ? (
          <p className="empty-cart-message">Your cart is empty.</p>
      ) : (
          cartItems.map((item, index) => {
            const price = typeof item.price === 'number' ? item.price : 0; // Fallback to 0
            return (
              <div key={index} className="cart-item">
                <img src={item.image} alt={item.name} className="cart-item-image" />
                <div className="cart-item-details">
                  <h3>{item.name}</h3>
                  <p>Price: ${price.toFixed(2)}</p> {/* Safely display the price */}
                  <div className="cart-item-quantity">
                    <button
                      className="quantity-button"
                      onClick={() => handleQuantityChange(index, item.quantity + 1)}
                    >
                      +
                    </button>
                    <span>&nbsp;{item.quantity}</span>
                    <button
                      className="quantity-button"
                      onClick={() => handleQuantityChange(index, item.quantity - 1)}
                      disabled={item.quantity <= 1} // Prevent going below 1
                    >
                      -
                    </button>
                  </div>
                  <button className="remove-button" onClick={() => handleRemoveItem(index)}>
                    Remove
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
      <div className="cart-total">
        <h2 className="cart-total">Total: ${totalPrice.toFixed(2)}</h2>
        <button className="checkout-button"><a href="/checkout">Check Out</a></button>
      </div>
      <Footer/>
    </div>
  );
};

export default Cart;
