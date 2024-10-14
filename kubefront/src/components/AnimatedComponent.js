// src/components/AnimatedComponent.js
import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { fadeIn, slideIn } from '../styles/animations';

// Styled-component para aplicar o background
const BackgroundWrapper = styled.div`
  background-image: url('/assets/your-background-image.jpg'); /* Certifique-se de que este caminho esteja correto */
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Faz o background cobrir toda a tela */
  padding: 20px;
  filter: brightness(0.8); /* Aumenta o contraste do fundo */
`;

const AnimatedDiv = styled(motion.div)`
  ${fadeIn}
  background-color: rgba(30, 0, 50, 0.8); /* Fundo semi-transparente roxo escuro */
  padding: 40px;
  border-radius: 20px;
  color: ${({ theme }) => theme.colors.white}; /* Texto em branco */
  text-align: center;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8);
  transition: transform 0.4s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9);
  }
`;

const Title = styled(motion.h2)`
  font-size: 2.5rem;
  color: ${({ theme }) => theme.colors.cyan}; /* Usando a cor ciano do tema */
  letter-spacing: 0.1em;
  text-shadow: 0 0 20px ${({ theme }) => theme.colors.cyan}, 0 0 30px ${({ theme }) => theme.colors.purple};
  margin-bottom: 15px;
`;

const Description = styled(motion.p)`
  font-size: 1.4rem;
  color: ${({ theme }) => theme.colors.lightPurple}; /* Usando a cor roxa clara do tema */
  letter-spacing: 0.05em;
  margin-top: 15px;
  text-shadow: 0 0 10px ${({ theme }) => theme.colors.lightPurple};
`;

const AnimatedComponent = () => {
  return (
    <BackgroundWrapper>
      <AnimatedDiv
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <Title
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          Bem-vindo ao jKpCutPro!
        </Title>
        <Description
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          Transforme seus vídeos com inteligência artificial.
        </Description>
      </AnimatedDiv>
    </BackgroundWrapper>
  );
};

export default AnimatedComponent;
