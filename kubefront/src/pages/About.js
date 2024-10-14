// src/pages/About.js
import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaLightbulb, FaHandshake, FaQuestionCircle } from 'react-icons/fa'; // Importando ícones

const AboutContainer = styled(motion.div)`
  padding: 50px;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.darkBlue}; // Fundo escuro
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); // Sombra mais pronunciada
  margin: 20px;
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.accent}; // Cor do título
  margin-bottom: 20px;
  font-size: 2.5rem; // Aumentar tamanho da fonte do título
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6); // Sombra para destaque
`;

const Section = styled.div`
  margin: 20px 0;
`;

const Description = styled.p`
  color: ${({ theme }) => theme.colors.text}; // Cor do texto
  font-size: 1.2rem;
  line-height: 1.6;
`;

const IconContainer = styled.div`
  font-size: 3rem;
  color: ${({ theme }) => theme.colors.secondary}; // Cor dos ícones
  margin-bottom: 10px;
`;

const Button = styled(motion.button)`
  padding: 10px 20px;
  background-color: ${({ theme }) => theme.colors.accent}; // Cor do botão
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 20px;
  transition: background-color 0.3s, transform 0.3s; // Adicionando transição para o efeito de hover

  &:hover {
    background-color: rgba(255, 255, 255, 0.2);
    transform: scale(1.05); // Efeito de zoom suave
  }
`;

const About = () => (
  <AboutContainer
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    <Title>Sobre Nós</Title>
    <Section>
      <IconContainer>
        <FaLightbulb />
      </IconContainer>
      <Description>
        Nossa missão é transformar a maneira como as pessoas interagem com vídeos, utilizando soluções de automação de vídeo baseadas em inteligência artificial.
      </Description>
    </Section>
    <Section>
      <IconContainer>
        <FaHandshake />
      </IconContainer>
      <Description>
        Valorizamos parcerias e colaborações, buscando sempre atender às necessidades dos nossos clientes com eficiência e inovação.
      </Description>
    </Section>
    <Section>
      <IconContainer>
        <FaQuestionCircle />
      </IconContainer>
      <Description>
        Se você tiver alguma dúvida ou quiser saber mais sobre nossos serviços, não hesite em entrar em contato!
      </Description>
    </Section>
    <Button 
      whileHover={{ scale: 1.1 }} 
      whileTap={{ scale: 0.95 }}
      onClick={() => window.location.href = '#contact'} // Link para seção de contato
    >
      Entre em Contato
    </Button>
  </AboutContainer>
);

export default About;
