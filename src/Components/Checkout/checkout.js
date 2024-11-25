import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../Checkout/checkout.css';
import Navbar from '../Navbar/navbar';
import Footer from '../Foooter/footer';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    phone_number: '',
    email: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    creditCard: '',
    pickupOption: 'home', // Only home delivery is available now
  });
  const [confirmationNumber, setConfirmationNumber] = useState('');
  const [deliveryDate, setDeliveryDate] = useState('');
  const [shippingCost] = useState(15); // Default shipping cost
  const navigate = useNavigate();

  useEffect(() => {
    const storedCartItems = JSON.parse(sessionStorage.getItem('cart')) || [];
    setCartItems(storedCartItems);

    // Calculate delivery date (14 days from now)
    const delivery = new Date();
    delivery.setDate(delivery.getDate() + 14);
    setDeliveryDate(delivery.toDateString());

    // Generate a random confirmation number
    setConfirmationNumber(`ORD-${Math.floor(Math.random() * 1000000)}`);

    // Check if user is logged in
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
    if (!isLoggedIn) {
      navigate('/login'); // Redirect to login page if not logged in
    }
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Calculate total price based on cart items and their quantities
  const totalPrice = cartItems.reduce((acc, item) => {
    const price = typeof item.price === 'number' ? item.price : 0; // Ensure it's a number
    return acc + (price * (item.quantity || 0)); // Safely handle undefined quantity
  }, 0);

  // Update shipping cost based on pickup option
  const finalShippingCost = formData.pickupOption === 'home' ? shippingCost : 0;
  const finalTotal = totalPrice + finalShippingCost;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const orderData = {
      user_id: localStorage.getItem('userId'),
      customer_name: formData.name,
      phone_number: formData.phone_number,
      email: formData.email,
      delivery_address: `${formData.address}, ${formData.city}, ${formData.state} - ${formData.zip}`,
      order_id: confirmationNumber,
      cart_items: cartItems.map(item => ({
        product_name: item.name, // Rename for consistency with backend
        quantity: item.quantity || 1, // Default to 1 if undefined
      })),
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();

      if (result.status === 'success') {
        alert(`Order placed! Confirmation Number: ${confirmationNumber}. Delivery Date: ${deliveryDate}`);
        sessionStorage.removeItem('cart');
        navigate('/');
      } else {
        alert('Order failed. Please try again.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Order failed. Please try again.');
    }
  };

  return (
      <div className="checkout-page">
        <Navbar />
        <h1>Checkout</h1>
        <div className="cart-items">
          {cartItems.map((item, index) => (
              <div key={index} className="cart-item">
                <img src={item.image} alt={item.name} />
                <div>
                  <h2>{item.name}</h2>
                  <p>Price: ${item.price ? item.price.toFixed(2) : 'N/A'}</p>
                  <p>Quantity: {item.quantity}</p>
                </div>
              </div>
          ))}
        </div>
        <h2>Total: ${totalPrice.toFixed(2)}</h2>

        <form onSubmit={handleSubmit}>
          <h2>Personal Information</h2>
          <label>
            Name:
            <input
                type="text"
                name="name"
                placeholder="Enter the name for your Delivery"
                value={formData.name}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            Phone Number:
            <input
                type="tel"
                name="phone_number"
                placeholder="Enter your phone number"
                value={formData.phone_number}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            Email:
            <input
                type="email"
                name="email"
                placeholder="Enter your email address"
                value={formData.email}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            Address:
            <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            City:
            <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            State:
            <input
                type="text"
                name="state"
                value={formData.state}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            Zip-Code:
            <input
                type="text"
                name="zip"
                value={formData.zip}
                onChange={handleInputChange}
                required
            />
          </label>
          <label>
            Credit Card:
            <input
                type="text"
                name="creditCard"
                value={formData.creditCard}
                onChange={handleInputChange}
                required
            />
          </label>

          {formData.pickupOption === 'home' && <h3>Delivery Fee: $15.00</h3>}
          <h2>Final Total: ${finalTotal.toFixed(2)}</h2>

          <button type="submit">Place Order</button>
        </form>
        {confirmationNumber && <div>Confirmation Number: {confirmationNumber}</div>}
        <Footer />
      </div>
  );
};

export default Checkout;