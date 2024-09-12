<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['video_file'])) {
    $file = $_FILES['video_file'];
    $filePath = $file['tmp_name'];
    
    // Envio do vídeo para o backend FastAPI
    $apiUrl = 'http://127.0.0.1:8000/upload-video/';
    $ch = curl_init($apiUrl);
    
    $postData = [
        'file' => curl_file_create($filePath)
    ];
    
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error: ' . curl_error($ch);
        curl_close($ch);
        exit;
    }
    curl_close($ch);
    
    $responseData = json_decode($response, true);
    if (!isset($responseData['file_path'])) {
        echo 'Error: Failed to upload video.';
        exit;
    }

    $videoPath = $responseData['file_path'];
    
    // Chamar o endpoint de processamento
    $processApiUrl = 'http://127.0.0.1:8000/process-video/';
    $ch = curl_init($processApiUrl);
    
    $processData = json_encode([
        'video_path' => $videoPath,
        'output_format' => 'tiktok' // ou 'youtube' conforme necessário
    ]);
    
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $processData);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    
    $processResponse = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error: ' . curl_error($ch);
        curl_close($ch);
        exit;
    }
    curl_close($ch);
    
    $processResponseData = json_decode($processResponse, true);
    if (!isset($processResponseData['message'])) {
        echo 'Error: Failed to process video.';
        exit;
    }

    echo 'Vídeo processado com sucesso: ' . htmlspecialchars($processResponseData['message']);
} else {
    echo 'Nenhum arquivo enviado.';
}