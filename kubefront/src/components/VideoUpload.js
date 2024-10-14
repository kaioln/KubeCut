// src/components/VideoUpload.js
import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const UploadContainer = styled(motion.div)`
  margin: 0 auto;
  padding: 20px;
  border: 2px dashed ${({ theme }) => theme.colors.accent};
  border-radius: 10px;
  transition: border-color 0.3s, background-color 0.3s, box-shadow 0.3s;
  cursor: pointer;
  text-align: center;
  position: relative;
  background-color: ${({ theme }) => theme.colors.darkBlue}; // Fundo da área de upload

  &:hover {
    border-color: ${({ theme }) => theme.colors.secondary};
    background-color: rgba(0, 0, 0, 0.2); // Fundo leve ao passar o mouse
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // Sombra ao passar o mouse
  }

  &:focus {
    outline: none;
    border-color: ${({ theme }) => theme.colors.secondary};
    box-shadow: 0 0 10px ${({ theme }) => theme.colors.secondary}; // Sombra ao focar
  }
`;

const UploadText = styled.p`
  color: ${({ theme }) => theme.colors.text};
  font-size: 1.4rem; // Aumentar o tamanho da fonte para melhor visibilidade
  font-weight: bold; // Tornar o texto mais destacado
  margin: 0; // Remover margens para melhor alinhamento
`;

const FeedbackText = styled.p`
  color: ${({ success }) => (success ? 'green' : 'red')};
  font-size: 1rem;
  margin-top: 10px;
  transition: color 0.3s; // Transição suave para o feedback
`;

const FileName = styled.p`
  color: ${({ theme }) => theme.colors.text};
  font-weight: bold;
  margin-top: 5px;
  font-size: 1.2rem; // Aumentar o tamanho da fonte do nome do arquivo
`;

const LoadingSpinner = styled.div`
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid ${({ theme }) => theme.colors.secondary};
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin: 10px auto;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const VideoUpload = () => {
  const [feedback, setFeedback] = useState('');
  const [fileName, setFileName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDrop = (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;

    if (files.length > 0) {
      const file = files[0];
      const validFormats = ['video/mp4', 'video/avi', 'video/mkv', 'video/webm']; // Formatos válidos

      if (validFormats.includes(file.type)) {
        setFileName(file.name);
        setLoading(true);
        setFeedback('Fazendo upload do vídeo...');

        // Simulação de upload de vídeo
        setTimeout(() => {
          setFeedback('Upload bem-sucedido!'); // Mensagem de sucesso
          setLoading(false);
        }, 2000); // Simulação de 2 segundos de upload
      } else {
        setFeedback('Erro: formato de vídeo não suportado.');
      }
    } else {
      setFeedback('Erro ao fazer upload. Tente novamente.'); // Mensagem de erro
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <UploadContainer
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      role="button"
      tabIndex={0}
      aria-label="Área de upload de vídeo"
    >
      <UploadText>Arraste e solte seus vídeos aqui!</UploadText>
      {loading && <LoadingSpinner />}
      {fileName && <FileName>Arquivo: {fileName}</FileName>}
      {feedback && <FeedbackText success={feedback.includes('sucesso')}>{feedback}</FeedbackText>}
    </UploadContainer>
  );
};

export default VideoUpload;
