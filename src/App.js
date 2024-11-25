import "./App.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Components/Home';
import Navbar from "./Components/Navbar/navbar";
import Login from './Components/Login/login';
import Create from './Components/Create-Account/create';
import Cart from './Components/Cart/cart';
import Checkout from './Components/Checkout/checkout';
import Chatbot from './Components/Chat/Chat';
import Footer from './Components/Foooter/footer';
import Orders from './Components/Orders/Orders'; // Import Orders component with capital O

function App() {
    return (
        <Router>
            {/* Navbar is rendered for all routes */}
            <Navbar />

            <Routes>
                {/* Home page route */}
                <Route path="/" index element={<Home />} />

                {/* Login and Create routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/create" element={<Create />} />

                {/* Cart and Checkout routes */}
                <Route path="/cart" element={<Cart />} />
                <Route path="/checkout" element={<Checkout />} />

                {/* Orders route */}
                <Route path="/orders" element={<Orders />} />

                {/* Chatbot and Footer routes */}
                <Route path="/chatbot" element={<Chatbot />} />
                <Route path="/footer" element={<Footer />} />
            </Routes>

        </Router>
    );
}

export default App;