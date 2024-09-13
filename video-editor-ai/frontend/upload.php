<?php
// Verifica se a requisição foi enviada por meio do método POST e se um arquivo de vídeo foi anexado.
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['video'])) {
    // Obtém o arquivo de vídeo enviado através do formulário.
    $video = $_FILES['video'];
    // Define o caminho onde o arquivo será armazenado temporariamente no servidor.
    $target_path = 'uploads/' . basename($video['name']);

    // Verifica se o diretório de uploads existe. Se não existir, cria o diretório com permissões apropriadas.
    if (!is_dir('uploads')) {
        mkdir('uploads', 0777, true);  // Cria o diretório 'uploads' se não existir, com permissões 0777 e subdiretórios, se necessário.
    }

    // Move o arquivo enviado para o diretório de uploads.
    if (move_uploaded_file($video['tmp_name'], $target_path)) {
        // Inicializa uma nova sessão cURL para fazer a requisição ao backend FastAPI para o upload do vídeo.
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:8000/upload-video/');  // Define a URL do endpoint FastAPI para upload de vídeo.
        curl_setopt($ch, CURLOPT_POST, 1);  // Define o método da requisição como POST.
        curl_setopt($ch, CURLOPT_POSTFIELDS, ['file' => new CURLFile($target_path)]);  // Define os campos de dados POST com o arquivo carregado.
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  // Retorna o resultado da requisição cURL como uma string.

        // Executa a requisição cURL e captura a resposta.
        $response = curl_exec($ch);
        if ($response === false) {
            // Exibe uma mensagem de erro se a requisição cURL falhar.
            echo 'cURL Error: ' . curl_error($ch);
        } else {
            // Exibe uma mensagem de sucesso com a resposta do backend.
            echo 'Video uploaded successfully. Response: ' . $response;
        }

        // Fecha a sessão cURL após a requisição ser concluída.
        curl_close($ch);
    } else {
        // Exibe uma mensagem de erro se falhar ao mover o arquivo para o diretório de uploads.
        echo 'Failed to move uploaded file.';
    }
} else {
    // Exibe uma mensagem de erro se nenhum vídeo foi enviado.
    echo 'No video uploaded.';
}
