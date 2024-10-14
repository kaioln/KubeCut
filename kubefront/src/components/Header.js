import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaBars, FaTimes, FaTwitter, FaLinkedin, FaGithub } from 'react-icons/fa';
import { Link } from 'react-scroll';
import { Tooltip } from 'react-tippy';
import 'react-tippy/dist/tippy.css';

// Container do cabeçalho
const HeaderContainer = styled(motion.header)`
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(20, 20, 20, 0.95); // Cor escura constante
  transition: background-color 0.4s ease, box-shadow 0.4s ease;
  box-shadow: ${({ isScrolling }) =>
    isScrolling ? '0 4px 12px rgba(0, 0, 0, 0.4)' : 'none'};
`;

// Logo
const Logo = styled(motion.h1)`
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.cyan};
  text-transform: uppercase;
  letter-spacing: 0.15em;
  text-shadow: 0 0 10px ${({ theme }) => theme.colors.cyan};
  cursor: pointer;
  transition: color 0.3s ease, text-shadow 0.3s ease;

  &:hover {
    color: ${({ theme }) => theme.colors.highlight};
    text-shadow: 0 0 20px ${({ theme }) => theme.colors.highlight};
  }
`;

// Navegação
const Nav = styled.nav`
  display: flex;
  gap: 3rem;
  align-items: center;

  a {
    font-size: 1.1rem;
    color: ${({ theme }) => theme.colors.white};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-decoration: none;
    position: relative;
    padding: 0.5rem 0;
    transition: color 0.3s ease, text-shadow 0.3s ease;

    &:hover {
      color: ${({ theme }) => theme.colors.highlight};
      text-shadow: 0 0 10px ${({ theme }) => theme.colors.highlight};
    }

    &::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: -4px;
      width: 0;
      height: 2px;
      background: ${({ theme }) => theme.colors.highlight};
      transition: width 0.3s ease;
    }

    &:hover::after {
      width: 100%;
    }
  }

  @media (max-width: 768px) {
    display: none; // Esconder no modo móvel
  }
`;

// Navegação móvel
const MobileNav = styled(motion.nav)`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: ${({ theme }) => theme.colors.darkPurple};
  padding: 1rem;
  border-radius: 8px;
  position: absolute;
  top: 70px;
  right: 2rem; // Alinhado à direita
  width: 220px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.6);
  transition: transform 0.3s ease; // Transição suave

  a {
    color: ${({ theme }) => theme.colors.white};
    text-decoration: none;
    text-transform: uppercase;

    &:hover {
      color: ${({ theme }) => theme.colors.highlight};
      text-shadow: 0 0 10px ${({ theme }) => theme.colors.highlight};
    }
  }
`;

// Toggle do Menu
const MenuToggle = styled.div`
  display: none;
  cursor: pointer;
  font-size: 2rem;
  color: ${({ theme }) => theme.colors.white};

  @media (max-width: 768px) {
    display: block; // Mostrar no modo móvel
  }
`;

// Ícones de redes sociais
const SocialIcons = styled.div`
  display: flex;
  gap: 1rem;

  a {
    color: ${({ theme }) => theme.colors.white};
    font-size: 1.5rem;
    transition: color 0.3s ease;

    &:hover {
      color: ${({ theme }) => theme.colors.highlight};
    }
  }
`;

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolling, setIsScrolling] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolling(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <HeaderContainer
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, type: 'spring' }}
      isScrolling={isScrolling}
    >
      <Logo whileHover={{ scale: 1.1 }} transition={{ duration: 0.3 }}>
        KubeCut
      </Logo>

      <Nav>
        <Tooltip title="Back to Home" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="home" smooth={true} duration={1000}>
            Home
          </Link>
        </Tooltip>
        <Tooltip title="Explore Features" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="features" smooth={true} duration={1000}>
            Features
          </Link>
        </Tooltip>
        <Tooltip title="See Testimonials" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="testimonials" smooth={true} duration={1000}>
            Testimonials
          </Link>
        </Tooltip>
        <Tooltip title="Learn About Us" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="about" smooth={true} duration={1000}>
            About Us
          </Link>
        </Tooltip>
        <Tooltip title="View Services" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="services" smooth={true} duration={1000}>
            Services
          </Link>
        </Tooltip>
        <Tooltip title="Contact Us" position="bottom" trigger="mouseenter" arrow={true} distance={18}>
          <Link to="contact" smooth={true} duration={1000}>
            Contact
          </Link>
        </Tooltip>
      </Nav>

      <SocialIcons>
        <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
          <FaTwitter />
        </a>
        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
          <FaLinkedin />
        </a>
        <a href="https://github.com" target="_blank" rel="noopener noreferrer">
          <FaGithub />
        </a>
      </SocialIcons>

      <MenuToggle onClick={toggleMenu}>
        {isOpen ? <FaTimes /> : <FaBars />}
      </MenuToggle>

      {isOpen && (
        <MobileNav
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
        >
          <Link to="home" smooth={true} duration={1000} onClick={toggleMenu}>
            Home
          </Link>
          <Link to="features" smooth={true} duration={1000} onClick={toggleMenu}>
            Features
          </Link>
          <Link to="testimonials" smooth={true} duration={1000} onClick={toggleMenu}>
            Testimonials
          </Link>
          <Link to="about" smooth={true} duration={1000} onClick={toggleMenu}>
            About Us
          </Link>
          <Link to="services" smooth={true} duration={1000} onClick={toggleMenu}>
            Services
          </Link>
          <Link to="contact" smooth={true} duration={1000} onClick={toggleMenu}>
            Contact
          </Link>
        </MobileNav>
      )}
    </HeaderContainer>
  );
};

export default Header;
