// src/components/Button.js
import React from 'react';
import styled, { css } from 'styled-components';
import { motion } from 'framer-motion';

const StyledButton = styled(motion.button)`
  background-color: var(--button-bg-color); /* Cor do fundo do botão */
  color: var(--text-color); /* Texto branco */
  border: 2px solid var(--highlight-color); /* Efeito de neon na borda */
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-shadow: 0 0 8px var(--highlight-color); /* Neon no texto */
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5); /* Sombra */
  position: relative;
  overflow: hidden;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.4s ease;
  z-index: 1;

  /* Efeitos de tamanhos dinâmicos */
  ${({ size }) =>
    size === 'small' &&
    css`
      padding: 8px 16px;
      font-size: 14px;
    `}

  ${({ size }) =>
    size === 'large' &&
    css`
      padding: 16px 32px;
      font-size: 18px;
    `}

  /* Efeito de hover com neon mais forte e mudança de cor */
  &:hover {
    background-color: var(--button-hover-color); /* Cor ao passar o mouse */
    border-color: var(--highlight-color); /* Mudança na borda */
    text-shadow: 0 0 15px var(--highlight-color); /* Neon mais forte */
    box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.7); /* Sombra maior */
    transform: translateY(-4px);
  }

  &:active {
    transform: translateY(1px);
    box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.3);
  }

  /* Efeito de onda de luz no hover */
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300%;
    height: 300%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent);
    transition: all 0.6s ease;
    transform: translate(-50%, -50%) scale(0);
    z-index: -1;
  }

  &:hover::before {
    transform: translate(-50%, -50%) scale(1);
  }

  &:disabled {
    background-color: rgba(142, 68, 173, 0.5);
    cursor: not-allowed;
    box-shadow: none;
    pointer-events: none;
  }
`;

const Button = ({ children, onClick, size, disabled }) => {
  return (
    <StyledButton
      onClick={onClick}
      size={size}
      disabled={disabled}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      {children}
    </StyledButton>
  );
};

export default Button;
