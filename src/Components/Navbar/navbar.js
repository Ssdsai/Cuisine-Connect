// import React, { useState, useEffect } from 'react';
// import { useNavigate, useLocation } from 'react-router-dom';
// import "./navbar.css";
//
// function Navbar() {
//   const [scrolled, setScrolled] = useState(false);
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const navigate = useNavigate();
//   const location = useLocation();
//
//   useEffect(() => {
//     const handleScroll = () => {
//       setScrolled(window.scrollY > 10);
//     };
//     window.addEventListener("scroll", handleScroll);
//     return () => window.removeEventListener("scroll", handleScroll);
//   }, []);
//
//   useEffect(() => {
//     const loggedInState = localStorage.getItem("isLoggedIn") === "true";
//     setIsLoggedIn(loggedInState);
//   }, [location]);
//
//   const handleNavigation = (e) => {
//     e.preventDefault();
//     const target = e.target.getAttribute("data-target");
//
//     if (location.pathname !== "/") {
//       navigate("/", { replace: true });
//       setTimeout(() => scrollToSection(target), 100);
//     } else {
//       scrollToSection(target);
//     }
//   };
//
//   const scrollToSection = (sectionId) => {
//     const section = document.getElementById(sectionId);
//     if (section) {
//       section.scrollIntoView({ behavior: "smooth" });
//     }
//   };
//
//   const handleLoginLogout = () => {
//     if (isLoggedIn) {
//       localStorage.setItem("isLoggedIn", "false");
//       setIsLoggedIn(false);
//       navigate("/"); // Redirect to home page after logout
//     } else {
//       navigate("/login"); // Redirect to login page
//     }
//   };
//
//   // Determine classes
//   const navbarClass = `navbar ${
//     location.pathname === '/'
//       ? scrolled ? 'scrolled' : ''
//       : 'non-home'
//   }`;
//
//   return (
//     <nav className={navbarClass}>
//       <div className="logo">Cuisine Connect</div>
//       <div className="menu">
//         <a href="/">Home</a>
//         <a href="/" data-target="cuisines" onClick={handleNavigation}>Cuisines</a>
//         <a href="/#contact">Contact</a>
//         <a href="/cart">Cart</a>
//         {!isLoggedIn && (
//           <a href="/login">Profile</a>
//         )}
//         {isLoggedIn && (
//           <button onClick={handleLoginLogout} className="logout-button">
//             Log Out
//           </button>
//         )}
//       </div>
//     </nav>
//   );
// }
//
// export default Navbar;


import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import "./navbar.css";

function Navbar() {
    const [scrolled, setScrolled] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 10);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    useEffect(() => {
        const loggedInState = localStorage.getItem("isLoggedIn") === "true";
        setIsLoggedIn(loggedInState);
    }, [location]);

    const handleNavigation = (e) => {
        e.preventDefault();
        const target = e.target.getAttribute("data-target");

        if (location.pathname !== "/") {
            navigate("/", { replace: true });
            setTimeout(() => scrollToSection(target), 100);
        } else {
            scrollToSection(target);
        }
    };

    const scrollToSection = (sectionId) => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ behavior: "smooth" });
        }
    };

    const handleLoginLogout = () => {
        if (isLoggedIn) {
            localStorage.setItem("isLoggedIn", "false");
            setIsLoggedIn(false);
            navigate("/"); // Redirect to home page after logout
        } else {
            navigate("/login"); // Redirect to login page
        }
    };

    // Determine classes
    const navbarClass = `navbar ${
        location.pathname === '/'
            ? scrolled ? 'scrolled' : ''
            : 'non-home'
    }`;

    return (
        <nav className={navbarClass}>
            <div className="logo">Cuisine Connect</div>
            <div className="menu">
                <a href="/">Home</a>
                <a href="/" data-target="cuisines" onClick={handleNavigation}>Cuisines</a>
                <a href="/#contact">Contact</a>
                <a href="/cart">Cart</a>
                {isLoggedIn && <a href="/orders">Orders</a>} {/* Add Orders link */}
                {!isLoggedIn && (
                    <a href="/login">Profile</a>
                )}
                {isLoggedIn && (
                    <button onClick={handleLoginLogout} className="logout-button">
                        Log Out
                    </button>
                )}
            </div>
        </nav>
    );
}

export default Navbar;