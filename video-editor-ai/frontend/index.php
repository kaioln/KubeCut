<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Aplicação para edição automática de vídeos para TikTok e YouTube Reels. Suba seus vídeos e obtenha cortes e legendas otimizados para cada plataforma.">
    <meta name="keywords" content="edição de vídeos, TikTok, YouTube Reels, legendas automáticas, edição automática">
    <title>jKpCutPro</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">jKpCutPro</div>
            <nav>
                <ul>
                    <li><a href="#features">Recursos</a></li>
                    <li><a href="#upload">Upload</a></li>
                    <li><a href="#testimonials">Depoimentos</a></li>
                    <li><a href="#faq">FAQ</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h2>Transforme Seus Vídeos de Forma Automática</h2>
            <p>Suba seus vídeos e deixe que nossa tecnologia cuide dos cortes e legendas, prontos para TikTok e YouTube Reels.</p>
            <a href="#upload" class="primary-btn">Comece Agora</a>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2>Recursos Principais</h2>
            <div class="feature-card">
                <h3>Edição Inteligente</h3>
                <p>Automatize os cortes e ajustes para as melhores práticas de TikTok e YouTube Reels.</p>
            </div>
            <div class="feature-card">
                <h3>Geração de Legendas</h3>
                <p>Obtenha legendas automáticas precisas e sincronizadas com o seu vídeo.</p>
            </div>
            <div class="feature-card">
                <h3>Interface Simples</h3>
                <p>Carregue seu vídeo e deixe o resto conosco. Rápido e fácil de usar.</p>
            </div>
        </div>
    </section>

    <section id="upload" class="upload-section">
        <div class="container">
            <h2>Faça o Upload do Seu Vídeo</h2>
            <p>Escolha o arquivo do vídeo que deseja processar e selecione a plataforma para a qual deseja otimizar.</p>
            <form class="upload-form" id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" id="file" accept="video/*" required aria-label="Escolha o arquivo de vídeo">
                <select name="output_format" id="output_format" required aria-label="Escolha o formato de saída">
                    <option value="tiktok">TikTok</option>
                    <option value="youtube">YouTube</option>
                </select>
                <button type="submit" class="upload-btn" aria-label="Enviar vídeo">Enviar Vídeo</button>
            </form>
            <div id="feedback" class="feedback"></div> <!-- Área para feedback -->
        </div>
    </section>

    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2>O que Nossos Usuários Dizem</h2>
            <div class="testimonial-carousel">
                <!-- Cartões de Testemunhos -->
                <div class="testimonial">
                    <p>"A edição automática é incrível! Consegui subir meus vídeos e obter resultados profissionais sem esforço."</p>
                    <div class="user">Ana Souza</div>
                </div>
                <div class="testimonial">
                    <p>"Um serviço fantástico para quem deseja otimizar seus vídeos para redes sociais sem complicação."</p>
                    <div class="user">João Silva</div>
                </div>
                <div class="testimonial">
                    <p>"Excelente ferramenta! Facilidade e rapidez na edição dos vídeos."</p>
                    <div class="user">Maria Oliveira</div>
                </div>
                <div class="testimonial">
                    <p>"A automação do processo de edição é um grande diferencial. Muito prático e eficiente!"</p>
                    <div class="user">Carlos Santos</div>
                </div>
                <div class="testimonial">
                    <p>"Adorei a facilidade de subir vídeos e receber cortes otimizados. Recomendo!"</p>
                    <div class="user">Fernanda Costa</div>
                </div>
                <div class="testimonial">
                    <p>"A integração com as plataformas sociais é perfeita. A edição automática é um verdadeiro tempo-saver."</p>
                    <div class="user">Juliana Almeida</div>
                </div>
            </div>
        </div>
    </section>

    <section id="faq" class="faq">
        <div class="container">
            <h2>Perguntas Frequentes</h2>
            <div class="faq-item">
                <h3>Como funciona a edição automática?</h3>
                <p>Nossa tecnologia analisa o vídeo e aplica cortes e ajustes baseados nas melhores práticas para cada plataforma.</p>
            </div>
            <div class="faq-item">
                <h3>Posso personalizar os cortes?</h3>
                <p>Atualmente, os cortes são automatizados, mas estamos trabalhando em opções de personalização para breve.</p>
            </div>
            <div class="faq-item">
                <h3>Qual o formato de vídeo aceito?</h3>
                <p>Aceitamos vídeos em formatos comuns como MP4, AVI, e MOV. Certifique-se de que o vídeo esteja em alta qualidade.</p>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 jKpCutPro. Todos os direitos reservados. | <a href="#">Privacidade</a> | <a href="#">Termos de Serviço</a></p>
        </div>
    </footer>

    <!-- Scripts para feedback e carrossel -->
    <script>
        // Função para fazer upload de vídeo e exibir feedback
        document.querySelector('#uploadForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Evita o envio padrão do formulário
            
            const formData = new FormData(this);
            
            fetch('http://localhost:8001/process-video/', { // Altere o URL para o endereço correto do FastAPI
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.output_path) {
                    document.getElementById('feedback').innerHTML = `<p>Vídeo processado com sucesso! Baixe o vídeo editado <a href="${data.output_path}" target="_blank">aqui</a>.</p>`;
                } else {
                    document.getElementById('feedback').innerHTML = `<p>Erro ao processar vídeo: ${data.detail}</p>`;
                }
            })
            .catch(error => {
                document.getElementById('feedback').innerHTML = `<p>Erro ao processar vídeo: ${error.message}</p>`;
            });
        });

        // Navegação do carrossel
        const carousel = document.querySelector('.testimonial-carousel');
        let isDragging = false;
        let startX, scrollLeft, lastX, velocity, lastTimestamp, animationFrameId;

        const inertia = () => {
            if (Math.abs(velocity) > 0.1) {
                carousel.scrollLeft -= velocity;
                velocity *= 0.95; // Reduz a velocidade para simular desaceleração
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
            const walk = (x - startX) * 2; // Ajuste a velocidade de rolagem
            carousel.scrollLeft = scrollLeft - walk;

            const now = Date.now();
            const deltaX = x - lastX;
            const deltaTime = now - lastTimestamp;

            velocity = deltaX / deltaTime;
            lastX = x;
            lastTimestamp = now;
        });

        document.addEventListener('keydown', (e) => {
            const step = 100; // Ajuste o valor de acordo com sua necessidade
            if (e.key === 'ArrowLeft') {
                carousel.scrollLeft -= step;
            } else if (e.key === 'ArrowRight') {
                carousel.scrollLeft += step;
            }
        });
    </script>
</body>
</html>
