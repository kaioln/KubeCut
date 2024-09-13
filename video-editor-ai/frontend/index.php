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
            <form class="upload-form" action="/upload-video/" method="post" enctype="multipart/form-data">
                <input type="file" name="file" id="file" accept="video/*" required aria-label="Escolha o arquivo de vídeo">
                <button type="submit" class="upload-btn" aria-label="Enviar vídeo">Enviar Vídeo</button>
            </form>
            <div id="feedback" class="feedback"></div> <!-- Área para feedback -->
        </div>
    </section>

    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2>O que Nossos Usuários Dizem</h2>
            <div class="testimonial-carousel">
                <!-- 20 Cartões de Testemunhos -->
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
                    <p>"A melhor solução para criar conteúdo dinâmico para as redes sociais."</p>
                    <div class="user">Pedro Santos</div>
                </div>
                <div class="testimonial">
                    <p>"Muito fácil de usar e os resultados são sempre impressionantes."</p>
                    <div class="user">Carla Lima</div>
                </div>
                <div class="testimonial">
                    <p>"Recomendo para quem busca otimização sem perder qualidade."</p>
                    <div class="user">Lucas Pereira</div>
                </div>
                <div class="testimonial">
                    <p>"A interface é intuitiva e o serviço é rápido. Muito satisfeito!"</p>
                    <div class="user">Juliana Costa</div>
                </div>
                <div class="testimonial">
                    <p>"Transformou a forma como edito meus vídeos para redes sociais."</p>
                    <div class="user">Marcos Almeida</div>
                </div>
                <div class="testimonial">
                    <p>"O melhor investimento para quem trabalha com criação de conteúdo."</p>
                    <div class="user">Fernanda Ribeiro</div>
                </div>
                <div class="testimonial">
                    <p>"A edição automática é um divisor de águas para meu trabalho."</p>
                    <div class="user">Gustavo Martins</div>
                </div>
                <div class="testimonial">
                    <p>"Ótima ferramenta para economizar tempo e obter resultados profissionais."</p>
                    <div class="user">Letícia Duarte</div>
                </div>
                <div class="testimonial">
                    <p>"A qualidade da edição é impecável e o processo é simples."</p>
                    <div class="user">Renato Souza</div>
                </div>
                <div class="testimonial">
                    <p>"Uma solução prática para quem precisa de vídeos bem editados rapidamente."</p>
                    <div class="user">Samantha Silva</div>
                </div>
                <div class="testimonial">
                    <p>"Excelente para quem quer otimizar seu trabalho sem complicações."</p>
                    <div class="user">Ricardo Fernandes</div>
                </div>
                <div class="testimonial">
                    <p>"A experiência de uso é fantástica e os resultados são consistentes."</p>
                    <div class="user">Tatiane Oliveira</div>
                </div>
                <div class="testimonial">
                    <p>"Facilitou muito a minha rotina de criação de vídeos."</p>
                    <div class="user">Eduardo Gomes</div>
                </div>
                <div class="testimonial">
                    <p>"Muito prático e eficiente. Recomendo para todos."</p>
                    <div class="user">Amanda Almeida</div>
                </div>
                <div class="testimonial">
                    <p>"Transforma a forma como produzo conteúdo para as redes."</p>
                    <div class="user">Joana Costa</div>
                </div>
                <div class="testimonial">
                    <p>"A melhor ferramenta que encontrei para edição de vídeos."</p>
                    <div class="user">Rodrigo Lima</div>
                </div>
                <div class="testimonial">
                    <p>"Simples de usar e com resultados que impressionam."</p>
                    <div class="user">Patrícia Silva</div>
                </div>
                <div class="testimonial">
                    <p>"Ótima opção para quem precisa de edição rápida e eficiente."</p>
                    <div class="user">Thiago Santos</div>
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
        // Feedback após envio de vídeo
        document.querySelector('.upload-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Evita o envio padrão do formulário
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => {
                  document.getElementById('feedback').innerHTML = `<p>Vídeo enviado com sucesso: ${data.file_path}</p>`;
              }).catch(error => {
                  document.getElementById('feedback').innerHTML = `<p>Erro ao enviar vídeo: ${error.message}</p>`;
              });
        });

        // Navegação do carrossel
        const carousel = document.querySelector('.testimonial-carousel');
        let isDragging = false;
        let startX, scrollLeft;

        carousel.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.pageX - carousel.offsetLeft;
            scrollLeft = carousel.scrollLeft;
        });

        carousel.addEventListener('mouseleave', () => {
            isDragging = false;
        });

        carousel.addEventListener('mouseup', () => {
            isDragging = false;
        });

        carousel.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - carousel.offsetLeft;
            const walk = (x - startX) * 2; // Ajuste a velocidade de rolagem
            carousel.scrollLeft = scrollLeft - walk;
        });

        // Navegação com as setas do teclado
        document.addEventListener('keydown', (e) => {
            const step = 100; // Ajuste o valor conforme necessário
            if (e.key === 'ArrowLeft') {
                carousel.scrollLeft -= step;
            } else if (e.key === 'ArrowRight') {
                carousel.scrollLeft += step;
            }
        });
    </script>
</body>
</html>
