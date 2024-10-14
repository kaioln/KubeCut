// src/pages/Contact.js
import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaEnvelope, FaUser, FaCommentDots } from 'react-icons/fa'; // Importando ícones

const ContactContainer = styled(motion.div)`
  padding: 50px;
  text-align: center;
  background-color: ${({ theme }) => theme.colors.darkBlue}; // Fundo escuro
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); // Sombra mais pronunciada
  margin: 20px;
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.accent}; // Cor do título
  margin-bottom: 20px;
  font-size: 2.5rem; // Aumentar tamanho da fonte do título
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); // Sombra para destaque
`;

const EmailText = styled.p`
  color: ${({ theme }) => theme.colors.text}; // Cor do texto
  font-size: 1.2rem;
  margin-bottom: 20px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const InputContainer = styled.div`
  position: relative;
  width: 80%;
  max-width: 400px;
  margin-bottom: 15px;
`;

const Input = styled.input`
  padding: 10px 40px; // Adicionando espaço para ícones
  border: 1px solid ${({ theme }) => theme.colors.accent}; // Cor da borda
  border-radius: 5px;
  width: 100%;
  font-size: 1rem; // Tamanho da fonte
  background-color: ${({ theme }) => theme.colors.lightBlue}; // Fundo do input
  color: ${({ theme }) => theme.colors.text}; // Cor do texto

  &::placeholder {
    color: ${({ theme }) => theme.colors.placeholder}; // Cor do placeholder
  }
`;

const Textarea = styled.textarea`
  padding: 10px 40px; // Adicionando espaço para ícones
  border: 1px solid ${({ theme }) => theme.colors.accent}; // Cor da borda
  border-radius: 5px;
  width: 100%;
  max-width: 400px;
  resize: none;
  font-size: 1rem; // Tamanho da fonte
  background-color: ${({ theme }) => theme.colors.lightBlue}; // Fundo do textarea
  color: ${({ theme }) => theme.colors.text}; // Cor do texto

  &::placeholder {
    color: ${({ theme }) => theme.colors.placeholder}; // Cor do placeholder
  }
`;

const Button = styled.button`
  padding: 10px 20px;
  background-color: ${({ theme }) => theme.colors.accent}; // Cor do botão
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s; // Adicionando transição suave

  &:hover {
    background-color: rgba(255, 255, 255, 0.2); // Efeito de hover
    transform: scale(1.05); // Efeito de zoom suave
  }
`;

const FeedbackText = styled.p`
  color: ${({ success }) => (success ? 'green' : 'red')};
  margin-top: 20px;
`;

const Contact = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [feedback, setFeedback] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Aqui você pode adicionar a lógica para enviar a mensagem
    if (name && email && message) {
      setFeedback('Mensagem enviada com sucesso!'); // Mensagem de sucesso
      setName('');
      setEmail('');
      setMessage('');
    } else {
      setFeedback('Por favor, preencha todos os campos.'); // Mensagem de erro
    }
  };

  return (
    <ContactContainer
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Title>Contato</Title>
      <EmailText>Entre em contato conosco pelo email: contato@kubecut.com</EmailText>
      <Form onSubmit={handleSubmit}>
        <InputContainer>
          <FaUser style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--highlight-color)' }} />
          <Input 
            type="text" 
            placeholder="Seu Nome" 
            required 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
          />
        </InputContainer>
        <InputContainer>
          <FaEnvelope style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--highlight-color)' }} />
          <Input 
            type="email" 
            placeholder="Seu Email" 
            required 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
          />
        </InputContainer>
        <InputContainer>
          <FaCommentDots style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--highlight-color)' }} />
          <Textarea 
            rows="4" 
            placeholder="Sua Mensagem" 
            required 
            value={message} 
            onChange={(e) => setMessage(e.target.value)} 
          />
        </InputContainer>
        <Button type="submit">Enviar Mensagem</Button>
        {feedback && <FeedbackText success={feedback.includes('sucesso')}>{feedback}</FeedbackText>}
      </Form>
    </ContactContainer>
  );
};

export default Contact;
