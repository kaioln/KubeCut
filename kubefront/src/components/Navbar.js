// src/components/Navbar.js
import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaBars, FaTimes } from 'react-icons/fa';

// Container do Navbar
const Nav = styled.nav`
  background-color: ${({ theme }) => theme.colors.darkPurple};
  padding: 1.5rem 2rem; // Aumentar o padding para mais espaçamento
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background-color 0.3s ease;
`;

// Título do Navbar
const Title = styled.h1`
  color: ${({ theme }) => theme.colors.cyan};
  margin: 0;
  font-size: 2.5rem; // Aumentar o tamanho do título
  font-weight: bold;

  @media (max-width: 768px) {
    font-size: 2rem; // Tamanho do título em telas pequenas
  }
`;

// Links de Navegação
const NavLinks = styled(motion.ul)`
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;

  @media (max-width: 768px) {
    display: ${({ isOpen }) => (isOpen ? 'flex' : 'none')};
    flex-direction: column;
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    background-color: ${({ theme }) => theme.colors.darkPurple};
    padding: 1rem 0;
    border-radius: 8px;
  }
`;

// Link Individual
const NavLink = styled(motion.li)`
  color: ${({ theme }) => theme.colors.white};
  text-decoration: none;
  font-size: 1.2rem;
  cursor: pointer;
  position: relative;

  &:hover {
    color: ${({ theme }) => theme.colors.cyan};
    transform: scale(1.1);
    transition: transform 0.2s ease, color 0.2s ease;

    &::after {
      content: '';
      position: absolute;
      left: 0;
      bottom: -4px;
      width: 100%;
      height: 2px;
      background: ${({ theme }) => theme.colors.cyan};
    }
  }
`;

// Ícone do Menu
const MenuIcon = styled.div`
  font-size: 1.8rem;
  color: ${({ theme }) => theme.colors.cyan};
  cursor: pointer;
  display: none;

  @media (max-width: 768px) {
    display: block;
  }
`;

// Botão de Call to Action
const CtaButton = styled.a`
  background-color: ${({ theme }) => theme.colors.highlight};
  color: ${({ theme }) => theme.colors.text};
  padding: 0.7rem 1.2rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: ${({ theme }) => theme.colors.highlightHover};
  }

  @media (max-width: 768px) {
    margin-top: 1rem;
  }
`;

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <Nav>
      <Title>KubeCut</Title>
      <MenuIcon onClick={toggleMenu}>
        {isOpen ? <FaTimes /> : <FaBars />}
      </MenuIcon>
      <NavLinks isOpen={isOpen} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }}>
        <NavLink whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <a href="#home">Home</a>
        </NavLink>
        <NavLink whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <a href="#features">Features</a>
        </NavLink>
        <NavLink whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <a href="#testimonials">Testimonials</a>
        </NavLink>
        <NavLink whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <a href="#about">About Us</a> {/* Adicionado novo link */}
        </NavLink>
        <NavLink whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
          <a href="#contact">Contact</a> {/* Adicionado novo link */}
        </NavLink>
      </NavLinks>
      <CtaButton href="#signup">Get Started</CtaButton> {/* Botão de chamada à ação */}
    </Nav>
  );
};

export default Navbar;
