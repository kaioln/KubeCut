<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editor de Vídeos</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <h1>Editor de Vídeos Automático</h1>
        <form action="process.php" method="post" enctype="multipart/form-data">
            <label for="video_file">Selecione o vídeo:</label>
            <input type="file" name="video_file" id="video_file" required>
            <button type="submit">Enviar Vídeo</button>
        </form>
        <div id="result">
            <?php
            if (isset($_GET['message'])) {
                echo "<p class='message'>" . htmlspecialchars($_GET['message']) . "</p>";
            }
            ?>
        </div>
    </div>
</body>
</html>
