<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Editor AI</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>Upload Video</h1>
    <form action="upload.php" method="POST" enctype="multipart/form-data">
        <input type="file" name="video" accept="video/*" required>
        <button type="submit">Upload</button>
    </form>
    
    <h2>Process Video</h2>
    <form action="process.php" method="POST">
        <input type="text" name="video_path" placeholder="Path to video file" required>
        <select name="output_format">
            <option value="tiktok">TikTok</option>
            <option value="youtube">YouTube</option>
        </select>
        <button type="submit">Process</button>
    </form>
</body>
</html>
