// src/styles/animations.js
import { keyframes } from 'styled-components';

// Animação de Fade In
const fadeInKeyframes = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

// Animação de Slide In
const slideInKeyframes = keyframes`
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
`;

// Animação de Scale Up
const scaleUpKeyframes = keyframes`
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
`;

// Estilos para animações
const fadeIn = `
  animation: ${fadeInKeyframes} 0.8s ease forwards;
`;

const slideIn = `
  animation: ${slideInKeyframes} 0.8s ease forwards;
`;

const scaleUp = `
  animation: ${scaleUpKeyframes} 0.8s ease forwards;
`;

// Exportando as animações
export { fadeIn, slideIn, scaleUp };
