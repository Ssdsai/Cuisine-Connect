import React, { useEffect, useState } from 'react';
import Footer from '../Foooter/footer'; // Import the Footer component
import './Orders.css';

function Orders() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        // Fetch orders data from the backend API
        const fetchOrders = async () => {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/orders'); // Replace with actual API endpoint
                const data = await response.json();
                setOrders(data);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
    }, []);

    return (
        <div className="orders-page">
            <div className="orders-content">
                <h1 className="orders-heading">Your Orders</h1>
                {orders.length > 0 ? (
                    <ul className="orders-list">
                        {orders.map((order, index) => (
                            <li key={index} className="order-item">
                                <h3 className="order-id">Order ID: {order.order_id}</h3>
                                <p className="order-customer-name">
                                    Customer Name: {order.customer_name}
                                </p>
                                <p className="order-delivery-address">
                                    Delivery Address: {order.delivery_address}
                                </p>
                                <p className="order-items-heading">Items:</p>
                                <ul className="order-items-list">
                                    {order.cart_items.map((item, i) => (
                                        <li key={i} className="order-item-detail">
                                            {item.product_name} - Quantity: {item.quantity}
                                        </li>
                                    ))}
                                </ul>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="no-orders-message">No orders found</p>
                )}
            </div>
            <Footer />
        </div>
    );
}

export default Orders;