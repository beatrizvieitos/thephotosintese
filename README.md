# 📸 The Photo Síntese - Portfolio Web App

Bem-vindos ao repositório do website **The Photo Síntese**. Esta é uma aplicação web de portfólio, desenvolvida para exibir trabalhos de fotografia e vídeo profissional, desenhada com foco na performance, responsividade e facilidade de manutenção de conteúdo.

## Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Jinja2 (Templating Engine)
* **Gestão de Dados:** JSON (para legendas dinâmicas) e Dicionários Python
* **Alojamento de Media:** Cloudinary (para otimização e streaming de vídeos/imagens sem sobrecarregar o servidor)
* **Servidor de Produção:** Gunicorn

## Funcionalidades Principais

* **Geração Dinâmica de Conteúdo:** As páginas de portfólio (`portfolioFoto.html` e `menuportfolio.html`) são geradas dinamicamente pelo Flask, lendo categorias e rotas a partir do `app.py`.
* **Legendas Centralizadas:** A gestão de nomes de clientes e títulos de álbuns é feita através de um ficheiro `legendas.json`, separando a lógica de código dos dados de apresentação.
* **Otimização de Media:** Integração com URLs do Cloudinary para servir vídeos de alta qualidade de forma fluida.
* **Design Responsivo e Clean:** Interface desenhada de raiz em CSS (`index.css`), adaptável a dispositivos móveis e desktops, com efeitos de *overlay* suaves nas galerias.
* **Script de Limpeza de Repositório:** Inclui um script personalizado (`magia.py`) criado para transformar ficheiros de media locais em ficheiros "fantasma" de 0 bytes, mantendo o repositório Git leve e rápido de clonar.

## Estrutura do Projeto

```text
├── app.py                  # Ficheiro principal da aplicação Flask (Rotas e Lógica)
├── magia.py                # Script utilitário para otimizar o peso dos ficheiros no Git
├── requirements.txt        # Dependências do projeto
├── legendas.json           # Base de dados em JSON para os títulos das fotos
├── static/
│   ├── index.css           # Folha de estilos global
│   └── assets/             # Imagens base (logos, capas) e vídeos (fantasmas)
└── templates/              # Ficheiros HTML com Jinja2
    ├── index.html          # Página Inicial
    ├── sobre.html          # Página Sobre Nós
    ├── contactos.html      # Página de Contactos
    ├── menuportfolio.html  # Menu de seleção de álbuns (Fotografia/Vídeo)
    └── portfolioFoto.html  # Galeria de visualização dos trabalhos
