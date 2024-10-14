// src/pages/Home.js
import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import Button from '../components/Button';
import Features from '../components/Features';
import Testimonials from '../components/Testimonials';
import Particles from 'react-tsparticles';

const HomeSection = styled.section`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  padding: 0 20px;
  position: relative;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(30, 0, 61, 0.9) 0%, rgba(10, 0, 20, 0.8) 100%); // Fundo em gradiente
`;

const Title = styled(motion.h1)`
  color: ${({ theme }) => theme.colors.accent}; // Cor de destaque
  font-size: 3rem; // Aumentando o tamanho do título
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8); // Sombra para maior destaque

  @media (max-width: 768px) {
    font-size: 2.5rem; // Tamanho ajustado para dispositivos menores
  }
`;

const Subtitle = styled(motion.p)`
  color: ${({ theme }) => theme.colors.text}; // Cor do texto
  font-size: 1.6rem; // Aumentando o tamanho do subtítulo
  margin: ${({ theme }) => theme.spacing(2)} 0; // Usando o sistema de espaçamento
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); // Sombra sutil

  @media (max-width: 768px) {
    font-size: 1.4rem; // Ajustando para dispositivos menores
  }
`;

const ButtonContainer = styled(motion.div)`
  margin-top: 20px; // Espaçamento entre o botão e o texto
`;

const Home = () => {
  return (
    <>
      <HomeSection>
        <Particles
          id="tsparticles"
          options={{
            background: { color: { value: "#1e003d" } },
            fpsLimit: 60,
            particles: {
              color: { value: "#ffffff" },
              links: { enable: true, color: "#ffffff", width: 1 },
              move: { enable: true, speed: 2, straight: false }, // Aumentar a velocidade
              size: { value: 5 }, // Aumentar o tamanho das partículas
              opacity: { value: 0.7 }, // Tornar as partículas mais visíveis
              number: { value: 150 }, // Aumenta o número de partículas
            },
          }}
        />
        <Title
          initial={{ opacity: 0, y: -100 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          Welcome to KubeCut
        </Title>
        <Subtitle
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          Automate your video processing with cutting-edge AI.
        </Subtitle>
        <ButtonContainer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
        >
          <Button onClick={() => alert("Iniciando a versão gratuita!")}>
            Try for Free
          </Button>
        </ButtonContainer>
      </HomeSection>
      <Features />
      <Testimonials />
    </>
  );
};

export default Home;
