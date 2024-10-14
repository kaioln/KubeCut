// src/components/Features.js
import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const Section = styled.section`
  padding: 5rem 3rem;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.darkPurple}; /* Fundo escuro */
  color: ${({ theme }) => theme.colors.white}; /* Texto branco */
  margin-bottom: 3rem; /* Espaçamento maior entre seções */
  border-radius: 20px;
  box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.5); /* Sombra mais intensa */
`;

const Title = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: ${({ theme }) => theme.colors.cyan}; /* Título com cor ciano brilhante */
  text-shadow: 0 0 10px ${({ theme }) => theme.colors.cyan}; /* Efeito neon no título */
`;

const FeatureList = styled.div`
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 3rem;
  margin-top: 3rem;

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
`;

const FeatureItem = styled(motion.div)`
  flex: 1 1 30%;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.4); /* Fundo semi-transparente */
  border-radius: 15px;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.4); /* Sombra ao redor do item */
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0px 12px 35px rgba(0, 0, 0, 0.6); /* Sombra mais intensa no hover */
  }

  h3 {
    font-size: 1.8rem;
    color: ${({ theme }) => theme.colors.purple}; /* Cor roxa vibrante no título */
    margin-bottom: 1rem;
    text-shadow: 0 0 8px ${({ theme }) => theme.colors.purple}; /* Efeito neon no título */
  }

  p {
    font-size: 1rem;
    color: ${({ theme }) => theme.colors.textSecondary}; /* Texto secundário mais claro */
  }

  /* Efeito de luz neon no hover */
  &:hover h3 {
    text-shadow: 0 0 12px ${({ theme }) => theme.colors.purple};
  }
`;

const Features = () => {
  return (
    <Section>
      <Title>Nossas Funcionalidades</Title>
      <FeatureList>
        {[{
          title: "Renderização Rápida",
          description: "Processamento de vídeos em tempo recorde com tecnologia de IA.",
        },
        {
          title: "Qualidade de Alta Definição",
          description: "Suporte para vídeos em 4K e otimização de desempenho.",
        },
        {
          title: "Fácil de Usar",
          description: "Interface intuitiva e responsiva para qualquer tipo de usuário.",
        }].map((feature, index) => (
          <FeatureItem
            key={index}
            initial={{ opacity: 0, y: 20 }} // Animação de entrada suave
            animate={{ opacity: 1, y: 0 }} // Estado final com fade-in
            transition={{ duration: 0.5, delay: index * 0.2 }} // Atraso para cada item
            whileHover={{ scale: 1.1 }} // Efeito de hover ampliado
          >
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </FeatureItem>
        ))}
      </FeatureList>
    </Section>
  );
};

export default Features;
