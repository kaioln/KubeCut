<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Aplicação para edição automática de vídeos para TikTok e YouTube Reels. Suba seus vídeos e obtenha cortes e legendas otimizados para cada plataforma.">
    <meta name="keywords" content="edição de vídeos, TikTok, YouTube Reels, legendas automáticas, edição automática">
    <title>Editor de Vídeos Automático</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <div class="logo">VideoEditPro</div>
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
                <input type="file" name="file" id="file" required>
                <button type="submit" class="upload-btn">Enviar Vídeo</button>
            </form>
        </div>
    </section>

    <section id="testimonials" class="testimonials">
        <div class="container">
            <h2>O que Nossos Usuários Dizem</h2>
            <div class="testimonial">
                <p>"A edição automática é incrível! Consegui subir meus vídeos e obter resultados profissionais sem esforço."</p>
                <div class="user">Ana Souza</div>
            </div>
            <div class="testimonial">
                <p>"Um serviço fantástico para quem deseja otimizar seus vídeos para redes sociais sem complicação."</p>
                <div class="user">João Silva</div>
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
            <p>&copy; 2024 VideoEditPro. Todos os direitos reservados. | <a href="#">Privacidade</a> | <a href="#">Termos de Serviço</a></p>
        </div>
    </footer>
</body>
</html>
