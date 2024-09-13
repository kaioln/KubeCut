<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['video'])) {
    $video = $_FILES['video'];
    $target_path = 'uploads/' . basename($video['name']);

    // Cria o diretório uploads se não existir
    if (!is_dir('uploads')) {
        mkdir('uploads', 0777, true);
    }

    if (move_uploaded_file($video['tmp_name'], $target_path)) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:8000/upload-video/');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, ['file' => new CURLFile($target_path)]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);

        if ($response === false) {
            echo 'cURL Error: ' . curl_error($ch);
        } else {
            echo 'Video uploaded successfully. Response: ' . $response;
        }

        curl_close($ch);
    } else {
        echo 'Failed to move uploaded file.';
    }
} else {
    echo 'No video uploaded.';
}
?>
