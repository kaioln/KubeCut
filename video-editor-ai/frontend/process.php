<?php
// Verifica se o método de requisição é POST e se o arquivo de vídeo foi enviado através do formulário.
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['video_file'])) {
    // Obtém o arquivo enviado através do formulário HTML.
    $file = $_FILES['video_file'];
    $filePath = $file['tmp_name'];  // Caminho temporário do arquivo no servidor.

    // URL do endpoint do backend FastAPI para upload de vídeos.
    $apiUrl = 'http://127.0.0.1:8000/upload-video/';
    
    // Inicializa uma nova sessão cURL para fazer a requisição de upload do vídeo.
    $ch = curl_init($apiUrl);
    
    // Prepara os dados para serem enviados na requisição cURL. O arquivo é enviado como uma nova instância de curl_file_create.
    $postData = [
        'file' => curl_file_create($filePath)  // Cria um arquivo cURL a partir do caminho temporário do arquivo.
    ];
    
    // Configurações da requisição cURL para fazer o upload do vídeo.
    curl_setopt($ch, CURLOPT_POST, true);  // Define o método como POST.
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);  // Define os campos de dados POST.
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  // Retorna o resultado como uma string.

    // Executa a requisição cURL e captura a resposta.
    $response = curl_exec($ch);
    // Verifica se houve um erro durante a execução da requisição.
    if (curl_errno($ch)) {
        echo 'Error: ' . curl_error($ch);  // Exibe o erro ocorrido.
        curl_close($ch);  // Fecha a sessão cURL.
        exit;  // Encerra o script.
    }
    curl_close($ch);  // Fecha a sessão cURL após a requisição ser concluída.
    
    // Decodifica a resposta JSON do backend FastAPI.
    $responseData = json_decode($response, true);
    // Verifica se a resposta contém o caminho do arquivo enviado.
    if (!isset($responseData['file_path'])) {
        echo 'Error: Failed to upload video.';  // Exibe uma mensagem de erro caso o upload falhe.
        exit;  // Encerra o script.
    }

    // Extrai o caminho do vídeo enviado da resposta.
    $videoPath = $responseData['file_path'];
    
    // URL do endpoint do backend FastAPI para processar o vídeo.
    $processApiUrl = 'http://127.0.0.1:8000/process-video/';
    
    // Inicializa uma nova sessão cURL para fazer a requisição de processamento do vídeo.
    $ch = curl_init($processApiUrl);
    
    // Prepara os dados para serem enviados na requisição de processamento.
    $processData = json_encode([
        'video_path' => $videoPath,  // Caminho do vídeo carregado que será processado.
        'output_format' => 'tiktok'  // Formato de saída desejado. Pode ser 'tiktok' ou 'youtube'.
    ]);
    
    // Configurações da requisição cURL para processar o vídeo.
    curl_setopt($ch, CURLOPT_POST, true);  // Define o método como POST.
    curl_setopt($ch, CURLOPT_POSTFIELDS, $processData);  // Define os campos de dados POST.
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  // Retorna o resultado como uma string.
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);  // Define o tipo de conteúdo como JSON.
    
    // Executa a requisição cURL e captura a resposta.
    $processResponse = curl_exec($ch);
    // Verifica se houve um erro durante a execução da requisição.
    if (curl_errno($ch)) {
        echo 'Error: ' . curl_error($ch);  // Exibe o erro ocorrido.
        curl_close($ch);  // Fecha a sessão cURL.
        exit;  // Encerra o script.
    }
    curl_close($ch);  // Fecha a sessão cURL após a requisição ser concluída.
    
    // Decodifica a resposta JSON do backend FastAPI.
    $processResponseData = json_decode($processResponse, true);
    // Verifica se a resposta contém a mensagem de sucesso do processamento.
    if (!isset($processResponseData['message'])) {
        echo 'Error: Failed to process video.';  // Exibe uma mensagem de erro caso o processamento falhe.
        exit;  // Encerra o script.
    }

    // Exibe uma mensagem de sucesso ao usuário informando que o vídeo foi processado com sucesso.
    echo 'Vídeo processado com sucesso: ' . htmlspecialchars($processResponseData['message']);
} else {
    // Exibe uma mensagem de erro se nenhum arquivo for enviado.
    echo 'Nenhum arquivo enviado.';
}
