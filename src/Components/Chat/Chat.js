import React, { useState, useEffect, useRef } from "react";
import "./Chat.css";

const Chat = () => {
    const [query, setQuery] = useState(""); // User input
    const [messages, setMessages] = useState([]); // Chat history
    const [loading, setLoading] = useState(false); // Loading state
    const [file, setFile] = useState(null); // Uploaded file
    const [fraudDetectionMode, setFraudDetectionMode] = useState(false); // Fraud detection flow trigger
    const [fraudDetails, setFraudDetails] = useState({ orderId: "", description: "" }); // Fraud inputs
    const [currentStep, setCurrentStep] = useState(1); // Step tracker for fraud flow
    const [showOrderForm, setShowOrderForm] = useState(false); // Toggle order form visibility
    const [orderDetails, setOrderDetails] = useState({
        name: "",
        email: "",
        phone: "",
        address: "",
        creditCard: "",
    }); // Order form state
    const chatWindowRef = useRef(null); // Chat window reference

    // Scroll to the bottom of the chat window when messages are updated
    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages]);

    // Function to parse bot responses into structured messages
    const parseBotResponse = (response) => {
        if (typeof response === "string") {
            return [{ type: "bot", text: response.trim() }];
        }

        if (Array.isArray(response)) {
            return response.map((item) => {
                const [textPart, imagePart] = item.split("\nImage URL: ");
                return {
                    type: "bot",
                    text: textPart.trim(),
                    imageUrl: imagePart ? imagePart.trim() : null, // Include the image URL if available
                };
            });
        }
        if (response.orderId) {
        const orderDetailsMessage = (
            <div className="order-details-container">
                <p><strong>Order ID:</strong> {response.orderId}</p>
                <p><strong>Food Item:</strong> {response.foodItem}</p>
                <p><strong>Quantity:</strong> {response.quantity}</p>
                <p><strong>Name:</strong> {response.name}</p>
                <p><strong>Email:</strong> {response.email}</p>
                <p><strong>Address:</strong> {response.deliveryAddress}</p>
            </div>
            );
            return [{ type: "bot", text: orderDetailsMessage }];
        }

        console.error("Unexpected response format:", response);
        return [
            { type: "bot", text: "Error: Unexpected response format from the server." },
        ];
    };

    const isFraudQuery = (text) => {
        const fraudKeywords = ["fraud", "issue", "problem", "damage", "broken"];
        return fraudKeywords.some((keyword) => text.toLowerCase().includes(keyword));
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim() && !fraudDetectionMode) return;

        if (!fraudDetectionMode) {
            // For general queries
            setMessages((prevMessages) => [...prevMessages, { type: "user", text: query }]);
            setLoading(true);

            try {
                const res = await fetch("http://127.0.0.1:5000/api/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ query, chat_history: messages }),
                });

                if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

                const data = await res.json();
                console.log("Backend Response:", data);

                if (isFraudQuery(query)) {
                    // Trigger fraud detection flow
                    setFraudDetectionMode(true);
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: "bot", text: "Please provide your Order ID to proceed." },
                    ]);
                } else if (data.response) {
                    const parsedMessages = parseBotResponse(data.response);
                    setMessages((prevMessages) => [...prevMessages, ...parsedMessages]);
                } else {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: "bot", text: "No response received from the server." },
                    ]);
                }
            } catch (error) {
                console.error("Error fetching bot response:", error);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: "bot", text: "Error fetching response. Please try again." },
                ]);
            } finally {
                setQuery("");
                setLoading(false);
            }
        } else {
            // Fraud detection step-by-step flow
            if (currentStep === 1 && fraudDetails.orderId.trim()) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: "user", text: `Order ID: ${fraudDetails.orderId}` },
                    { type: "bot", text: "Please provide a description of the issue." },
                ]);
                setCurrentStep(2);
            } else if (currentStep === 2 && fraudDetails.description.trim()) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: "user", text: `Description: ${fraudDetails.description}` },
                    { type: "bot", text: "Please upload an image of the issue." },
                ]);
                setCurrentStep(3);
            } else if (currentStep === 3 && file) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { type: "user", text: `Image uploaded: ${file.name}` },
                    { type: "bot", text: "Submitting your details for review. Please wait..." },
                ]);
                setLoading(true);

                try {
                    const formData = new FormData();
                    formData.append("query", "fraud detection");
                    formData.append("order_id", fraudDetails.orderId);
                    formData.append("description", fraudDetails.description);
                    formData.append("image", file);

                    const res = await fetch("http://127.0.0.1:5000/api/query", {
                        method: "POST",
                        body: formData,
                    });

                    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

                    const data = await res.json();
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        {
                            type: "bot",
                            text: `Decision: ${data.decision}`,
                            details: {
                                orderId: fraudDetails.orderId,
                                description: fraudDetails.description,
                                image: URL.createObjectURL(file),
                            },
                        },
                    ]);
                } catch (error) {
                    console.error("Error submitting fraud details:", error);
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { type: "bot", text: "Error processing your request. Please try again." },
                    ]);
                } finally {
                    setFraudDetectionMode(false);
                    setFraudDetails({ orderId: "", description: "" });
                    setFile(null);
                    setCurrentStep(1);
                    setLoading(false);
                }
            }
        }
    };

    const handleFileUpload = (e) => {
        const uploadedFile = e.target.files[0];
        if (uploadedFile) setFile(uploadedFile);
    };

    const handleFraudDetailsChange = (e) => {
        const { name, value } = e.target;
        setFraudDetails((prev) => ({ ...prev, [name]: value }));
    };

    const handleAddToCart = (itemName) => {
        alert(`"${itemName}" added to your cart!`);
        setShowOrderForm(true);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setOrderDetails((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleOrderSubmit = (e) => {
        e.preventDefault();
        setMessages((prevMessages) => [
            ...prevMessages,
            { type: "bot", text: "Your order has been placed successfully! ORD-7891011" },
        ]);
        setOrderDetails({
            name: "",
            email: "",
            phone: "",
            address: "",
            creditCard: "",
        });
        setShowOrderForm(false);
    };

    return (
        <div className="chat-container">
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`chat-message ${
                            message.type === "user" ? "user-message" : "bot-message"
                        }`}
                    >
                        <div className="message-content">
                            <p>{message.text}</p>
                            {message.imageUrl && (
                                <>
                                    <img
                                        src={message.imageUrl}
                                        alt="Food item"
                                        className="food-image"
                                    />
                                    <button
                                        className="add-to-cart-button"
                                        onClick={() => handleAddToCart(message.text.split(" - ")[0])}
                                    >
                                        Add to Cart
                                    </button>
                                </>
                            )}
                            {message.details && (
                                <div className="details-container">
                                    <p><strong>Order ID:</strong> {message.details.orderId}</p>
                                    <p><strong>Description:</strong> {message.details.description}</p>
                                    {message.details.image && (
                                        <img
                                            src={message.details.image}
                                            alt="Uploaded"
                                            className="uploaded-image"
                                        />
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {loading && <div className="bot-message">Bot is typing...</div>}
                {showOrderForm && (
                    <div className="order-form">
                        <form onSubmit={handleOrderSubmit}>
                            <h3>Enter Your Details</h3>
                            <label>
                                Name:
                                <input
                                    type="text"
                                    name="name"
                                    value={orderDetails.name}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Email:
                                <input
                                    type="email"
                                    name="email"
                                    value={orderDetails.email}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Phone:
                                <input
                                    type="tel"
                                    name="phone"
                                    value={orderDetails.phone}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Address:
                                <input
                                    type="text"
                                    name="address"
                                    value={orderDetails.address}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <label>
                                Credit Card:
                                <input
                                    type="text"
                                    name="creditCard"
                                    value={orderDetails.creditCard}
                                    onChange={handleInputChange}
                                    required
                                />
                            </label>
                            <button type="submit" className="submit-button">
                                Submit
                            </button>
                        </form>
                    </div>
                )}
            </div>
            <form onSubmit={handleSubmit} className="chat-input-container">
                {!fraudDetectionMode ? (
                    <>
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Ask a question..."
                            className="chat-input"
                            disabled={loading}
                        />
                        <button type="submit" className="send-button" disabled={loading}>
                            Send
                        </button>
                    </>
                ) : (
                    <>
                        {currentStep === 1 && (
                            <input
                                type="text"
                                name="orderId"
                                value={fraudDetails.orderId}
                                onChange={handleFraudDetailsChange}
                                placeholder="Enter Order ID"
                                className="chat-input"
                                required
                            />
                        )}
                        {currentStep === 2 && (
                            <input
                                type="text"
                                name="description"
                                value={fraudDetails.description}
                                onChange={handleFraudDetailsChange}
                                placeholder="Enter issue description"
                                className="chat-input"
                                required
                            />
                        )}
                        {currentStep === 3 && (
                            <input
                                type="file"
                                className="file-upload"
                                onChange={handleFileUpload}
                                required
                            />
                        )}
                        <button type="submit" className="send-button" disabled={loading}>
                            {currentStep === 3 ? "Submit Details" : "Next"}
                        </button>
                    </>
                )}
            </form>
        </div>
    );
};

export default Chat;