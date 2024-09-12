<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $video_path = $_POST['video_path'];
    $output_format = $_POST['output_format'];

    $data = json_encode(['video_path' => $video_path, 'output_format' => $output_format]);

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'http://127.0.0.1:8000/process-video/');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    $response = curl_exec($ch);
    curl_close($ch);

    echo 'Video processed successfully. Response: ' . $response;
} else {
    echo 'No data received.';
}
