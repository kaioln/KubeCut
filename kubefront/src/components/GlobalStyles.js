// src/styles/GlobalStyles.js
import { createGlobalStyle } from 'styled-components';
import '@fontsource/orbitron'; // Fonte Orbitron para títulos
import '@fontsource/poppins'; // Fonte Poppins para corpo
import wallpaper from '../assets/wallpaper.jpg'; // Imagem de fundo

const GlobalStyles = createGlobalStyle`
  :root {
    --primary-color: #6a1b9a; // Roxo escuro
    --secondary-color: #9c27b0; // Roxo médio
    --highlight-color: #ba68c8; // Roxo claro
    --background-color: rgba(10, 10, 20, 0.95); // Fundo escuro
    --text-color: #ffffff; // Texto branco
    --button-bg-color: #8e44ad; // Cor do fundo do botão
    --button-hover-color: #c0392b; // Cor do botão ao passar o mouse
    --link-hover-color: #f1c40f; // Cor do link ao passar o mouse
    --shadow-color: rgba(0, 0, 0, 0.3); // Cor da sombra
    --muted-text: rgba(255, 255, 255, 0.7); // Texto menos intenso
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif; // Fonte padrão para o corpo
  }

  body {
    background: url(${wallpaper}) no-repeat center center fixed; // Usando a imagem como fundo
    background-size: cover; // Cobre toda a área
    color: var(--text-color);
    line-height: 1.6;
    font-size: 16px; // Tamanho padrão da fonte
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: 'Orbitron', sans-serif; // Fonte para títulos
    color: var(--highlight-color);
    text-transform: uppercase;
    margin-bottom: 1rem; // Espaçamento inferior para títulos
    letter-spacing: 1px; // Espaçamento entre letras
    text-shadow: 0 0 15px rgba(186, 104, 200, 0.5); // Sombra de texto
  }

  a {
    color: var(--highlight-color);
    text-decoration: none;
    transition: color 0.3s ease, text-shadow 0.3s ease, transform 0.2s ease; // Transições suaves
  }

  a:hover {
    text-decoration: underline;
    color: var(--link-hover-color); // Cor ao passar o mouse
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.5); // Sombra de texto
    transform: scale(1.05); // Aumento ao passar o mouse
  }

  button {
    background-color: var(--button-bg-color);
    color: var(--text-color);
    border: none;
    border-radius: 10px; // Bordas arredondadas
    padding: 12px 24px; // Espaçamento interno
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease; // Transições suaves
    box-shadow: 0 4px 15px var(--shadow-color); // Sombra no botão
    font-size: 1rem; // Tamanho padrão da fonte do botão
  }

  button:hover {
    background-color: var(--button-hover-color); // Cor ao passar o mouse
    transform: scale(1.05); // Aumento ao passar o mouse
    box-shadow: 0 6px 20px var(--shadow-color); // Sombra mais intensa
  }

  .container {
    max-width: 1200px; // Largura máxima do container
    margin: auto; // Centraliza o container
    padding: 20px; // Espaçamento interno
  }

  section {
    padding: 40px 0; // Espaçamento entre seções
    margin: 20px 10px; // Margem lateral
    border-radius: 10px; // Bordas arredondadas
    background-color: rgba(255, 255, 255, 0.05); // Fundo levemente diferente para seções
    box-shadow: 0 4px 15px var(--shadow-color); // Sombra nas seções
  }

  ul {
    list-style: none; // Remove marcadores da lista
    padding: 0;
  }

  li {
    margin: 10px 0; // Espaçamento entre itens da lista
  }

  // Estilos de tabela
  table {
    width: 100%; // Tabela ocupa 100% da largura
    border-collapse: collapse; // Colapsa bordas
    margin: 20px 0; // Margem em cima e embaixo
  }

  th, td {
    padding: 15px; // Espaçamento interno nas células
    text-align: left; // Alinhamento à esquerda
    border-bottom: 1px solid var(--shadow-color); // Borda inferior nas células
  }

  th {
    background-color: var(--secondary-color); // Fundo para cabeçalhos
    color: var(--text-color); // Cor do texto
    font-weight: bold; // Negrito
  }

  // Adicionando estilos responsivos
  @media (max-width: 768px) {
    body {
      font-size: 90%; // Reduz o tamanho da fonte em telas menores
    }

    h1, h2, h3, h4, h5, h6 {
      margin-bottom: 0.5rem; // Menor espaçamento em telas pequenas
    }

    button {
      font-size: 0.9rem; // Ajuste do tamanho da fonte do botão
    }
  }
`;

export default GlobalStyles;
