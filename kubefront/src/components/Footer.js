// src/components/Footer.js
import React from 'react';
import styled from 'styled-components';
import { FaInstagram, FaTwitter, FaFacebookF, FaLinkedin, FaGithub } from 'react-icons/fa';

const FooterContainer = styled.footer`
  background-color: ${({ theme }) => theme.colors.secondaryDark}; 
  color: ${({ theme }) => theme.colors.text};
  text-align: center;
  padding: 1rem 2rem;
  position: relative;
  width: 100%;
  box-shadow: 0 -6px 25px rgba(0, 0, 0, 0.4);
  border-top: 3px solid ${({ theme }) => theme.colors.highlight};
  transition: all 0.3s ease;
  z-index: 10;
  display: flex; /* Usar flexbox para distribuir as seções */
  flex-direction: column;
  align-items: center; /* Centralizar o conteúdo */
  
  &:hover {
    background-color: ${({ theme }) => theme.colors.secondaryHover};
  }
`;

const FooterContent = styled.div`
  display: flex;
  flex-direction: row; /* Alinhamento horizontal */
  justify-content: space-between; /* Espalhar o conteúdo */
  align-items: flex-start; /* Alinhamento no topo */
  width: 100%; /* Usar toda a largura disponível */
  max-width: 1200px; /* Limitar a largura máxima */
  margin: 0 auto; /* Centralizar */
  padding: 1rem; /* Adicionando padding ao conteúdo */
`;

const SocialIcons = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;

  a {
    color: ${({ theme }) => theme.colors.text};
    margin: 0 10px; 
    font-size: 1.5rem; 
    transition: transform 0.4s ease, color 0.3s ease;
    position: relative;
    display: inline-block;

    &::after {
      content: '';
      position: absolute;
      bottom: -4px;
      left: 50%;
      transform: translateX(-50%);
      width: 0%;
      height: 2px;
      background-color: ${({ theme }) => theme.colors.highlight};
      transition: width 0.3s ease;
    }

    &:hover {
      color: ${({ theme }) => theme.colors.highlight};
      transform: translateY(-2px); 
      
      &::after {
        width: 100%;
      }
    }
  }
`;

const FooterText = styled.p`
  margin: 0;
  font-size: 0.9rem; 
  opacity: 0.85;
  letter-spacing: 1px;
  color: ${({ theme }) => theme.colors.mutedText};
`;

const FooterLinks = styled.div`
  display: flex;
  flex-direction: column; /* Alinhamento vertical */
  align-items: center; /* Centralizar os links */
  gap: 0.5rem; /* Espaçamento entre os links */

  a {
    color: ${({ theme }) => theme.colors.text};
    font-size: 0.8rem; 
    text-decoration: none;
    transition: color 0.3s ease;

    &:hover {
      color: ${({ theme }) => theme.colors.highlight};
    }
  }
`;

const FooterSections = styled.div`
  display: flex;
  justify-content: space-between; /* Espaçar as seções */
  flex-wrap: wrap; /* Permitir quebra de linha se necessário */
  gap: 2rem; /* Espaçamento entre as seções */

  div {
    flex: 1; /* Permitir que as divs cresçam igualmente */
    min-width: 150px; /* Largura mínima para as seções */
    
    h4 {
      margin-bottom: 0.3rem; 
      font-size: 1rem; 
      color: ${({ theme }) => theme.colors.highlight};
    }

    a {
      margin: 0.3rem 0; 
      color: ${({ theme }) => theme.colors.text};
      text-decoration: none;
      transition: color 0.3s ease;

      &:hover {
        color: ${({ theme }) => theme.colors.highlight};
      }
    }
  }
`;

const SubscribeForm = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 0.5rem; 

  input {
    padding: 0.5rem;
    border: none;
    border-radius: 4px;
    margin-bottom: 0.3rem; 
    width: 250px; 
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);

    &:focus {
      outline: none;
      box-shadow: 0 0 5px ${({ theme }) => theme.colors.highlight};
    }
  }

  button {
    padding: 0.5rem 0.8rem; 
    border: none;
    border-radius: 4px;
    background-color: ${({ theme }) => theme.colors.highlight};
    color: white;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: ${({ theme }) => theme.colors.highlightDark};
    }
  }
`;

const Footer = () => {
  return (
    <FooterContainer>
      <FooterContent>
        <SocialIcons>
          <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">
            <FaInstagram />
          </a>
          <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer">
            <FaTwitter />
          </a>
          <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">
            <FaFacebookF />
          </a>
          <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer">
            <FaLinkedin />
          </a>
          <a href="https://www.github.com" target="_blank" rel="noopener noreferrer">
            <FaGithub />
          </a>
        </SocialIcons>

        <FooterSections>
          <div>
            <h4>Sobre Nós</h4>
            <a href="/about">Quem Somos</a>
            <a href="/team">Nossa Equipe</a>
            <a href="/careers">Carreiras</a>
          </div>
          <div>
            <h4>Nossos Serviços</h4>
            <a href="/services">Serviços</a>
            <a href="/pricing">Preços</a>
            <a href="/portfolio">Portfólio</a>
          </div>
          <div>
            <h4>FAQ</h4>
            <a href="/faq">Perguntas Frequentes</a>
            <a href="/support">Suporte</a>
          </div>
        </FooterSections>

        <SubscribeForm>
          <input
            type="email"
            placeholder="Inscreva-se para atualizações"
            required
          />
          <button type="submit">Inscrever</button>
        </SubscribeForm>

        <FooterLinks>
          <a href="/privacy-policy">Política de Privacidade</a>
          <a href="/terms-of-service">Termos de Serviço</a>
          <a href="/contact">Contato</a>
        </FooterLinks>

        <FooterText>&copy; 2024 KubeCut. Todos os direitos reservados.</FooterText>
      </FooterContent>
    </FooterContainer>
  );
};

export default Footer;
