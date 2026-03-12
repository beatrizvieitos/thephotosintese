import os
from flask import Flask, render_template
from urllib.parse import quote 

app = Flask(__name__)

# Configuração dos caminhos
IMAGE_FOLDER = 'static/assets/img'
VIDEO_FOLDER = 'static/assets/videos'

# Dicionário para as capas do MENU
CAPAS = {
    'casamentos': 'weddings.png',
    'baptizados': 'bapti.jpg',
    'eventos': 'events.jpg',
    'festas de aniversário': 'festaanos.jpg',
    'espetáculos e Concertos': 'espet.jpg',
    'eventos corporativos': 'corporativo.jpg',
    'Sessões Fotográficas': 'sessoes.jpg',
    'os-casamentos': 'wedvideo.jpg',
    'os-baptizados': 'bapvideo.jpg'
}

# Links para vídeos no Cloudinary
LINKS_VIDEOS = {
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282255/AnabelaRui.mp4',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282236/AnaJoao.mp4',
    'PatriciaDiogo.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282230/PatriciaDiogo.mp4',
    'VivianeJunior.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282229/VivianeJunior.mp4',
}

# Legendas (vazio por enquanto)
legendas = {}

# Capas para vídeos (vazio por enquanto)
CAPAS_VIDEOS = {}

# Constantes para Cloudinary
CLOUDINARY_IMG_BASE = "https://res.cloudinary.com/dilatofg5/image/upload"
CLOUDINARY_VID_BASE = "https://res.cloudinary.com/dilatofg5/video/upload"


@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')


@app.route('/portfolio/<categoria>')
def menu_categorias(categoria):
    """Menu de subcategorias para fotografia ou vídeo"""
    
    # Define as subcategorias para cada tipo de portfolio
    if categoria == 'fotografia':
        subcategorias = [
            'casamentos', 
            'baptizados', 
            'eventos', 
            'espetáculos e Concertos', 
            'festas de aniversário', 
            'eventos corporativos', 
            'Sessões Fotográficas'
        ]
    else:  # categoria == 'video'
        subcategorias = ['os-casamentos', 'os-baptizados']
    
    # Prepara os dados para o template
    dados = {}
    for sub in subcategorias:
        dados[sub] = {
            'capa': CAPAS.get(sub, 'default.jpg')
        }
    
    return render_template('menuportfolio.html', categoria=categoria, dados=dados)


@app.route('/portfolio/<categoria>/<subcategoria>')
def ver_trabalhos(categoria, subcategoria):
    """Exibe os trabalhos (fotos ou vídeos) de uma subcategoria"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define a pasta base conforme a categoria
    if categoria == 'fotografia':
        base_folder = IMAGE_FOLDER
        cloudinary_base = CLOUDINARY_IMG_BASE
    else:
        base_folder = VIDEO_FOLDER
        cloudinary_base = CLOUDINARY_VID_BASE
    
    path = os.path.join(base_dir, base_folder, subcategoria)
    
    print(f"\n[DEBUG] A procurar em: {path}", flush=True)

    itens = []
    
    if os.path.exists(path):
        arquivos = os.listdir(path)
        print(f"[DEBUG] Ficheiros encontrados: {arquivos}", flush=True)
        
        for ficheiro in arquivos:
            if ficheiro.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.webm')):
                # Para vídeos, verifica se tem link específico
                if categoria == 'video' and ficheiro in LINKS_VIDEOS:
                    link_externo = LINKS_VIDEOS[ficheiro]
                else:
                    # Para imagens ou vídeos sem link específico, usa o Cloudinary
                    # Nota: O Cloudinary pode precisar de transformações ou paths específicos
                    # Este é um formato genérico - ajuste conforme necessário
                    file_url = quote(ficheiro)
                    link_externo = f"{cloudinary_base}/{file_url}"
                
                # Título a partir do nome do ficheiro (remove extensão)
                titulo = os.path.splitext(ficheiro)[0].replace('-', ' ').replace('_', ' ').title()
                
                itens.append({
                    'titulo': legendas.get(ficheiro, titulo),
                    'imagem': link_externo,
                    'poster': CAPAS_VIDEOS.get(ficheiro, None)  # Para vídeos com poster
                })
    else:
        print(f"[DEBUG] ERRO: Pasta não encontrada: {path}", flush=True)
        # Tenta criar a pasta se não existir? Talvez não seja boa ideia
    
    return render_template(
        'portfolioFoto.html', 
        categoria=categoria, 
        subcategoria=subcategoria, 
        itens=itens, 
        tipo=categoria
    )


@app.route('/sobre')
def sobre():
    """Página Sobre Nós"""
    return render_template('sobre.html')


@app.route('/contactos')
def contactos():
    """Página de Contactos"""
    return render_template('contactos.html')


if __name__ == '__main__':
    app.run(debug=True)