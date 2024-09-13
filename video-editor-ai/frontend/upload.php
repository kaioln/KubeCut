<?php
// Configurações
$uploadDirectory = 'uploads/';
$allowedFileTypes = ['video/mp4', 'video/mkv', 'video/avi']; // Tipos de vídeo permitidos

// Verifica se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file']) && isset($_POST['output_format'])) {
        $file = $_FILES['file'];
        $outputFormat = $_POST['output_format'];
        $targetFile = $uploadDirectory . basename($file['name']);
        
        // Verifica se o arquivo é um vídeo válido
        if (in_array($file['type'], $allowedFileTypes)) {
            if (move_uploaded_file($file['tmp_name'], $targetFile)) {
                // Chama a API FastAPI para processar o vídeo
                $apiUrl = 'http://localhost:8001/process-video/'; // URL da sua API FastAPI
                
                // Dados a serem enviados para a API FastAPI
                $data = [
                    'video_path' => $targetFile,
                    'output_format' => $outputFormat
                ];

                // Inicializa a sessão cURL
                $ch = curl_init($apiUrl);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_POST, true);
                curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
                curl_setopt($ch, CURLOPT_HTTPHEADER, [
                    'Content-Type: application/json',
                ]);

                // Envia o pedido
                $response = curl_exec($ch);
                $error = curl_error($ch);
                $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE); // Código HTTP da resposta
                curl_close($ch);

                // Verifica se houve erro com a requisição
                if ($httpCode != 200) {
                    echo '<p>Erro ao processar o vídeo. Código HTTP: ' . $httpCode . '</p>';
                    echo '<p>Detalhes do erro: ' . htmlspecialchars($error) . '</p>';
                } else {
                    // Exibe a resposta da API
                    $responseData = json_decode($response, true);
                    if (isset($responseData['output_path'])) {
                        echo '<p>Vídeo processado com sucesso! <a href="' . htmlspecialchars($responseData['output_path']) . '" target="_blank">Baixe o vídeo editado aqui</a>.</p>';
                    } else {
                        echo '<p>Resposta inesperada da API: ' . htmlspecialchars($response) . '</p>';
                    }
                }
            } else {
                echo '<p>Erro ao mover o arquivo para o diretório de upload.</p>';
            }
        } else {
            echo '<p>Tipo de arquivo não permitido. Apenas vídeos MP4, MKV e AVI são permitidos.</p>';
        }
    } else {
        echo '<p>Por favor, selecione um vídeo e uma plataforma.</p>';
    }
} else {
    echo '<p>Não foi possível processar o pedido. Tente novamente.</p>';
}
