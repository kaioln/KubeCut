// src/App.js
import React from 'react';
import styled, { ThemeProvider } from 'styled-components';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Features from './components/Features';
import Testimonials from './components/Testimonials';
import GlobalStyles from './components/GlobalStyles'; 
import { theme } from './styles/theme'; 
import wallpaper from './assets/wallpaper.jpg'; // Importe a imagem de fundo

const LayoutContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative; // Necessário para o posicionamento do fundo
  overflow: hidden; // Evita que o conteúdo transborde
`;

const BackgroundImage = styled.div`
  position: absolute; // Posiciona a imagem no fundo
  top: 0;
  left: 0;
  width: 100%; // Cobre toda a largura
  height: 100%; // Cobre toda a altura
  background-image: url(${wallpaper}); // Usa a imagem como fundo
  background-size: cover; // Cobre todo o contêiner sem distorcer
  background-position: center; // Centraliza a imagem
  z-index: -1; // Coloca a imagem atrás do conteúdo
  filter: brightness(0.7); // Escurece a imagem para melhorar a legibilidade do texto
`;

const MainContent = styled.main`
  flex: 1;
  margin-top: 70px; // Espaço para o cabeçalho fixo
  padding: ${({ theme }) => theme.spacing(4)}; // Usando o sistema de espaçamento do tema
  background-color: rgba(0, 0, 0, 0.6); // Cor de fundo semitransparente para dar destaque ao conteúdo
  border-radius: 10px; // Adiciona bordas arredondadas
  box-shadow: ${({ theme }) => theme.shadows.medium}; // Sombra média para destacar o conteúdo
`;

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles />
      <LayoutContainer>
        <BackgroundImage /> {/* Adicione a imagem de fundo */}
        <Header />
        <MainContent>
          <Home />
          <Features />
          <Testimonials />
        </MainContent>
        <Footer />
      </LayoutContainer>
    </ThemeProvider>
  );
};

export default App;
