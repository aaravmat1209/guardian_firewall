import React, { useState, useEffect } from 'react';
import '../styles/Navbar.css';

const Navbar = ({ onGetStarted }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className={`navbar ${isScrolled ? 'navbar-scrolled' : ''}`}>
      <div className="navbar-container">
        {/* Logo with Mascot - EXACT Quantra positioning */}
        <div className="navbar-logo">
          <img 
            src="/guardian_logo.png" 
            alt="Guardian AI Angel" 
            className="navbar-mascot"
          />
        </div>

        {/* Navigation Links - EXACT Quantra spacing */}
        <ul className="navbar-menu">
          <li className="navbar-item">
            <a href="#meet-guardian" className="navbar-link">
              MASCOT
            </a>
          </li>
          <li className="navbar-item">
            <a href="#demo" className="navbar-link">
              DEMO
            </a>
          </li>
          <li className="navbar-item">
            <a href="#features" className="navbar-link">
              FEATURES
            </a>
          </li>
          <li className="navbar-item">
            <a href="#contact" className="navbar-link">
              CONTACT
            </a>
          </li>
        </ul>

        {/* CTA Button - EXACT Quantra style */}
        <div className="navbar-actions">
          <button onClick={onGetStarted} className="btn btn-primary navbar-btn">
            GET STARTED
          </button>
        </div>

        {/* Mobile Menu Button */}
        <button 
          className="mobile-menu-btn"
          onClick={toggleMobileMenu}
          aria-label="Toggle mobile menu"
        >
          <span className={`hamburger ${isMobileMenuOpen ? 'active' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        {/* Mobile Menu */}
        <div className={`mobile-menu ${isMobileMenuOpen ? 'active' : ''}`}>
          <ul className="mobile-menu-list">
            <li>
              <a href="#meet-guardian" onClick={toggleMobileMenu}>MASCOT</a>
            </li>
            <li>
              <a href="#demo" onClick={toggleMobileMenu}>DEMO</a>
            </li>
            <li>
              <a href="#features" onClick={toggleMobileMenu}>FEATURES</a>
            </li>
            <li>
              <a href="#contact" onClick={toggleMobileMenu}>CONTACT</a>
            </li>
            <li>
              <button className="btn btn-primary" onClick={() => { onGetStarted(); toggleMobileMenu(); }}>
                GET STARTED
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
