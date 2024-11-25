import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './slider.css';

function HomeSlider() {
  const images = [
    'https://royalmahal.co.uk/wp-content/uploads/2023/01/indian-restaurant-scaled-e1670322083921.jpg', // Indian
    'https://png.pngtree.com/background/20230611/original/pngtree-italian-and-italian-food-as-well-other-fresh-produce-arranged-on-picture-image_3156990.jpg', // Italian
    'https://wallpapers.com/images/hd/food-4k-spdnpz7bhmx4kv2r.jpg', // Mexican
    'https://www.tastingtable.com/img/gallery/19-traditional-thai-dishes-you-should-know-about/l-intro-1675720327.jpg', // Thai
    'https://www.thetakeout.com/img/gallery/the-takeouts-guide-to-eating-korean-food-like-a-korean/l-intro-1724783140.jpg', // Korean
    'https://financesonline.com/uploads/2014/06/food4.jpg', // Japanese
    'https://media.cnn.com/api/v1/images/stellar/prod/gettyimages-1273516682.jpg?c=16x9&q=h_833,w_1480,c_fill', // American
    'https://assets.epicurious.com/photos/624d9590857fa7e509238b59/16:9/w_2560%2Cc_limit/RegionalChinese_HERO_033122_31320.jpg', // Chinese
    'https://images.squarespace-cdn.com/content/v1/55adab46e4b0d3eba6318941/1625935466674-8ZQ4SI68CCLSZNCVDJIT/Food-platter-e1604016303456.jpg?format=1500w' // Miscellaneous
  ];

  const settings = {
    autoplay: true,
    autoplaySpeed: 2500, // Increase time between transitions to 5 seconds
    infinite: true,
    dots: true,
    arrows: false,
    fade: true,
    pauseOnHover: false,
    speed: 2000 // Slow down the fade transition to 2 seconds
  };

  return (
      <div className="slider">
        <Slider {...settings}>
          {images.map((image, index) => (
              <div key={index} className="slider-item">
                <img src={image} alt={`Slide ${index + 1}`} className="slider-image" />
                <div className="slider-title">Cuisine Connect</div>
              </div>
          ))}
        </Slider>
      </div>
  );
}

export default HomeSlider;