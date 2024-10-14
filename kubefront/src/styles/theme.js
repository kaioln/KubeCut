// src/styles/theme.js

export const theme = {
  colors: {
    primary: '#6a1b9a',          // Cor primária
    secondary: '#9c27b0',        // Cor secundária
    highlight: '#ba68c8',         // Cor de destaque
    background: 'rgba(10, 10, 20, 0.9)', // Cor de fundo
    text: '#ffffff',              // Cor do texto principal
    textSecondary: '#b0bec5',     // Cor do texto secundário
    border: '#e0e0e0',            // Cor das bordas
    shadow: 'rgba(0, 0, 0, 0.5)', // Cor da sombra
    darkPurple: '#1e003d',        // Roxo escuro para backgrounds ou destaques
    lightPurple: '#d1c4e9',       // Roxo claro para textos e elementos
    cyan: '#00bcd4',              // Cor ciana para destaques adicionais
    neonGreen: '#39ff14',         // Verde neon para destaques
    neonBlue: '#00e0ff',          // Azul neon para elementos interativos
  },
  typography: {
    fontFamily: "'Roboto', sans-serif", // Fonte padrão
    fontSize: '16px',                     // Tamanho de fonte padrão
    fontWeightRegular: 400,               // Peso da fonte regular
    fontWeightBold: 700,                  // Peso da fonte bold
    lineHeight: 1.5,                      // Altura da linha para melhor legibilidade
  },
  spacing: (factor) => `${0.25 * factor}rem`, // Função de espaçamento
  breakpoints: {
    sm: '576px',   // Pequenos dispositivos
    md: '768px',   // Médios dispositivos
    lg: '992px',   // Grandes dispositivos
    xl: '1200px',  // Extra grandes dispositivos
  },
  shadows: {
    small: '0 2px 5px rgba(0, 0, 0, 0.1)',   // Sombra pequena
    medium: '0 4px 10px rgba(0, 0, 0, 0.2)', // Sombra média
    large: '0 6px 15px rgba(0, 0, 0, 0.3)',  // Sombra grande
  },
  transitions: {
    easeIn: 'ease-in',                    // Transição fácil
    easeOut: 'ease-out',                  // Transição difícil
    easeInOut: 'ease-in-out',             // Transição fácil em ambos os sentidos
    duration: '0.3s',                     // Duração padrão de transição
  },
};
