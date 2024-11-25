import React from "react";
import "../Foooter/footer.css";


function Footer() {
  return (
    <div id="container"
    style={{
              marginLeft: '-10px',  // Adjust this value to move the button further right        marginLeft: '217px', marginTop: '-20px'
    marginTop: '12px'
            }}>
      
      <footer>
        <div className="footer-bottom">
          <p>
            &copy;2024.{" "}
            <a href=" ">
              All rights Reserved.
            </a>{" "}
            Cuisine Connect
          </p>
        </div>
      </footer>
    </div>
  );
}

export default Footer;
