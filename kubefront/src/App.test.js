// src/App.test.js
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders welcome message', () => {
  render(<App />);
  const welcomeElement = screen.getByText(/welcome to jkpcutpro/i); // Substituindo pelo texto que deve aparecer na Home
  expect(welcomeElement).toBeInTheDocument();
});

test('renders features section', () => {
  render(<App />);
  const featuresElement = screen.getByText(/features/i); // Verificando se a seção de Features é renderizada
  expect(featuresElement).toBeInTheDocument();
});

test('renders testimonials section', () => {
  render(<App />);
  const testimonialsElement = screen.getByText(/testimonials/i); // Verificando se a seção de Testimonials é renderizada
  expect(testimonialsElement).toBeInTheDocument();
});
