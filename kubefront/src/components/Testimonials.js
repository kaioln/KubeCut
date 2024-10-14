// src/components/Testimonials.js
import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion'; // Importando a biblioteca framer-motion
import { FaStar } from 'react-icons/fa'; // Ícone de estrela para avaliação

// Seção dos Testemunhos
const TestimonialSection = styled.section`
  padding: 4rem 2rem;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.darkBlue}; // Cor de fundo
  color: ${({ theme }) => theme.colors.white}; // Cor do texto
  margin-bottom: 2rem;
  border-radius: 15px;
  box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.2);
`;

// Título da Seção
const Title = styled.h2`
  font-size: 2.5rem; // Aumentar o tamanho da fonte
  margin-bottom: 2rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.cyan}; // Cor do título
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); // Sombra para destaque
`;

// Lista de Testemunhos
const TestimonialList = styled.div`
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;

  @media (max-width: 768px) {
    flex-direction: column; // Colocar em coluna em telas pequenas
    align-items: center; // Centralizar os itens
  }
`;

// Item do Testemunho
const TestimonialItem = styled(motion.div)`
  flex: 1 1 30%;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.1); // Fundo com leve transparência
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  // Efeito de transformação ao passar o mouse
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.3);
  }

  @media (max-width: 768px) {
    flex: 1 1 90%; // Ocupa mais espaço em telas pequenas
  }
`;

// Citação do Testemunho
const Quote = styled.p`
  font-style: italic;
  margin: 1rem 0;
  font-size: 1.1rem; // Ajustar o tamanho da fonte da citação
`;

// Nome do Cliente
const ClientName = styled.h4`
  margin: 0.5rem 0 1rem 0;
  font-weight: normal;
  color: ${({ theme }) => theme.colors.cyan}; // Cor do nome
`;

// Avaliação
const Rating = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;

  svg {
    color: #f1c40f; // Cor das estrelas
    margin: 0 2px; // Margem entre as estrelas
  }
`;

const Testimonials = () => {
  const testimonialsData = [
    {
      text: "Serviço excepcional! Transformou meus vídeos.",
      name: "Cliente A",
      rating: 5,
    },
    {
      text: "Rápido e eficiente. Super recomendo!",
      name: "Cliente B",
      rating: 4,
    },
    {
      text: "A qualidade é incrível. Muito satisfeito!",
      name: "Cliente C",
      rating: 5,
    },
  ];

  return (
    <TestimonialSection>
      <Title>Nossos Clientes Falam</Title>
      <TestimonialList>
        {testimonialsData.map((testimonial, index) => (
          <TestimonialItem
            key={index}
            initial={{ opacity: 0, y: 20 }} // Animação inicial
            animate={{ opacity: 1, y: 0 }} // Animação ao entrar
            transition={{ duration: 0.5, delay: index * 0.2 }} // Duração da animação
          >
            <Quote>{`"${testimonial.text}"`}</Quote>
            <ClientName>- {testimonial.name}</ClientName>
            <Rating>
              {[...Array(testimonial.rating)].map((_, i) => (
                <FaStar key={i} />
              ))}
            </Rating>
          </TestimonialItem>
        ))}
      </TestimonialList>
    </TestimonialSection>
  );
};

export default Testimonials;
