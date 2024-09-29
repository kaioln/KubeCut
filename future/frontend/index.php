<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Application for automatic video editing for TikTok and YouTube Reels. Upload your videos and get optimized cuts and captions for each platform.">
    <meta name="keywords" content="video editing, TikTok, YouTube Reels, automatic captions, automated editing">
    <title>jKpCutPro</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">jKpCutPro</div>
            <nav>
                <ul>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#upload">Upload</a></li>
                    <li><a href="#testimonials">Testimonials</a></li>
                    <li><a href="#faq">FAQ</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h2>Transform Your Videos Automatically</h2>
            <p>Upload your videos and let our technology handle the cuts and captions, ready for TikTok and YouTube Reels.</p>
            <a href="#upload" class="primary-btn">Get Started</a>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2>Main Features</h2>
            <div class="feature-card">
                <h3>Smart Editing</h3>
                <p>Automate cuts and adjustments for optimal TikTok and YouTube Reels practices.</p>
            </div>
            <div class="feature-card">
                <h3>Caption Generation</h3>
                <p>Get accurate and synchronized automatic captions for your video.</p>
            </div>
            <div class="feature-card">
                <h3>Simplified Interface</h3>
                <p>Upload your video and leave the rest to us. Fast and easy to use.</p>
            </div>
        </div>
    </section>

    <section id="upload" class="upload-section">
        <div class="container">
            <h2>Upload Your Video</h2>
            <p>Select the video file you want to process and choose the platform you want to optimize for.</p>
            <form class="upload-form" id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" id="file" accept="video/*" required aria-label="Choose video file">
                <select name="output_format" id="output_format" required aria-label="Choose output format">
                    <option value="tiktok">TikTok</option>
                    <option value="youtube">YouTube</option>
                </select>
                <button type="submit" class="upload-btn" aria-label="Submit video">Submit Video</button>
            </form>
            <div id="feedback" class="feedback"></div> <!-- Feedback area -->
        </div>
    </section>

    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2>What Our Users Say</h2>
            <div class="testimonial-carousel">
                <!-- Testimonial Cards -->
                <div class="testimonial">
                    <p>"The automatic editing is amazing! I was able to upload my videos and get professional results effortlessly."</p>
                    <div class="user">Ana Souza</div>
                </div>
                <div class="testimonial">
                    <p>"A fantastic service for anyone wanting to optimize their videos for social media without hassle."</p>
                    <div class="user">João Silva</div>
                </div>
                <div class="testimonial">
                    <p>"Excellent tool! Ease and speed in video editing."</p>
                    <div class="user">Maria Oliveira</div>
                </div>
                <div class="testimonial">
                    <p>"The automation of the editing process is a major plus. Very practical and efficient!"</p>
                    <div class="user">Carlos Santos</div>
                </div>
                <div class="testimonial">
                    <p>"Loved the ease of uploading videos and receiving optimized cuts. Highly recommend!"</p>
                    <div class="user">Fernanda Costa</div>
                </div>
                <div class="testimonial">
                    <p>"The integration with social platforms is perfect. Automatic editing is a true time-saver."</p>
                    <div class="user">Juliana Almeida</div>
                </div>
            </div>
        </div>
    </section>

    <section id="faq" class="faq">
        <div class="container">
            <h2>Frequently Asked Questions</h2>
            <div class="faq-item">
                <h3>How does the automatic editing work?</h3>
                <p>Our technology analyzes the video and applies cuts and adjustments based on best practices for each platform.</p>
            </div>
            <div class="faq-item">
                <h3>Can I customize the cuts?</h3>
                <p>Currently, cuts are automated, but we are working on customization options for the near future.</p>
            </div>
            <div class="faq-item">
                <h3>What video formats are accepted?</h3>
                <p>We accept common video formats like MP4, AVI, and MOV. Ensure the video is in high quality.</p>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 jKpCutPro. All rights reserved. | <a href="#">Privacy</a> | <a href="#">Terms of Service</a></p>
        </div>
    </footer>

    <!-- Scripts for feedback and carousel -->
    <script>
        // Function to handle video upload and display feedback
        document.querySelector('#uploadForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            
            const formData = new FormData(this);
            
            fetch('process.php', { // URL updated to call process.php
                method: 'POST',
                body: formData
            })
            .then(response => response.text()) // Expecting plain text response
            .then(data => {
                document.getElementById('feedback').innerHTML = data; // Directly set HTML content
            })
            .catch(error => {
                document.getElementById('feedback').innerHTML = `<p>Error processing video: ${error.message}</p>`;
            });
        });

        // Carousel navigation
        const carousel = document.querySelector('.testimonial-carousel');
        let isDragging = false;
        let startX, scrollLeft, lastX, velocity, lastTimestamp, animationFrameId;

        const inertia = () => {
            if (Math.abs(velocity) > 0.1) {
                carousel.scrollLeft -= velocity;
                velocity *= 0.95; // Reduce velocity to simulate easing
                animationFrameId = requestAnimationFrame(inertia);
            } else {
                cancelAnimationFrame(animationFrameId);
            }
        };

        carousel.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.pageX - carousel.offsetLeft;
            scrollLeft = carousel.scrollLeft;
            lastX = startX;
            velocity = 0;
            lastTimestamp = Date.now();
            cancelAnimationFrame(animationFrameId);
        });

        carousel.addEventListener('mouseleave', () => {
            if (isDragging) {
                isDragging = false;
                inertia();
            }
        });

        carousel.addEventListener('mouseup', () => {
            if (isDragging) {
                isDragging = false;
                inertia();
            }
        });

        carousel.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - carousel.offsetLeft;
            const walk = (x - startX) * 2; // Adjust scroll speed
            carousel.scrollLeft = scrollLeft - walk;

            const now = Date.now();
            const deltaX = x - lastX;
            const deltaTime = now - lastTimestamp;

            velocity = deltaX / deltaTime;
            lastX = x;
            lastTimestamp = now;
        });

        document.addEventListener('keydown', (e) => {
            const step = 100; // Adjust value as needed
            if (e.key === 'ArrowLeft') {
                carousel.scrollLeft -= step;
            } else if (e.key === 'ArrowRight') {
                carousel.scrollLeft += step;
            }
        });
    </script>
</body>
</html>
