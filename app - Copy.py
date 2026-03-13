import os
from flask import Flask, render_template
from urllib.parse import quote 
import json

app = Flask(__name__)

def carregar_legendas():
    try:
        with open('legendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
# Configuração dos caminhos
IMAGE_FOLDER = 'static/assets/img'
VIDEO_FOLDER = 'static/assets/videos'

# Dicionário para as capas do MENU
CAPAS = {
    'casamentos': 'weddings.png',
    'baptizados': 'bapti.jpg',
    'eventos': 'events.jpg',
    'festas de aniversário': 'festaanos.jpg',
    'espetáculos': 'espet.jpg',
    'eventos corporativos': 'corporativo.jpg',
    'sessões fotográficas': 'sessoesfoto.jpg',
    'os-casamentos': 'wedvideo.jpg',
    'os-baptizados': 'bapvideo.jpg'
}

# Links para vídeos no Cloudinary
LINKS_VIDEOS = {
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282255/AnabelaRui.mp4',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282236/AnaJoao.mp4',
    'PatriciaDiogo.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282235/PatriciaDiogo.mp4',
    'JuniorVivianne.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282245/JuniorVivianne.mp4'
}

# Poster/Capa dos vídeos no Cloudinary (imagens)
CAPAS_VIDEOS = {
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400674/Anabela_e_Rui.png',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400693/anaejoao.jpg',
    'VivianeJunior.mp4' : 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400856/vivianejunior.jpg' ,
    'PatriciaDiogo.mp4' : 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400855/catarinadiogo.jpg',
}

@app.route('/')
def home():
    """Página inicial"""
    return render_template('index.html')


@app.route('/portfolio/<categoria>')
def menu_categorias(categoria):
    """Página intermédia que mostra as subcategorias (ex: Casamentos, Baptizados)"""
    
    dados = {}
    base_folder = IMAGE_FOLDER if categoria == 'fotografia' else VIDEO_FOLDER
    
    if os.path.exists(base_folder):
        subcategorias = [d for d in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, d))]
        
        for sub in subcategorias:
            capa = CAPAS.get(sub, f"{sub}.jpg") 
            dados[sub] = {'capa': capa}
            
    return render_template('menuportfolio.html', categoria=categoria, dados=dados)


@app.route('/portfolio/<categoria>/<subcategoria>')
def ver_trabalhos(categoria, subcategoria):
    # 1. URLs base limpas do Cloudinary (Sem versões v1741... para evitar erros)
    CLOUDINARY_BASE_IMG = "https://res.cloudinary.com/dilatofg5/image/upload"
    CLOUDINARY_BASE_VID = "https://res.cloudinary.com/dilatofg5/video/upload"
    
    base_folder = IMAGE_FOLDER if categoria == 'fotografia' else VIDEO_FOLDER
    path = os.path.join(base_folder, subcategoria)
    itens = []
    
    # Carregamos as legendas do ficheiro externo JSON
    todas_as_legendas = carregar_legendas()
    # Filtramos apenas as legendas desta pasta específica (ex: baptizados)
    legendas_da_pasta = todas_as_legendas.get(subcategoria, {})
    
    if os.path.exists(path):
        try:
            ficheiros = os.listdir(path)
            
            # Filtramos por extensões dependendo se é fotografia ou vídeo
            if categoria == 'video':
                ficheiros = [f for f in ficheiros if f.lower().endswith(('.mp4', '.mov', '.webm'))]
                cloudinary_base = CLOUDINARY_BASE_VID
            else:
                ficheiros = [f for f in ficheiros if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                cloudinary_base = CLOUDINARY_BASE_IMG
            
            ficheiros.sort() # Mantém a ordem alfabética
            
            for ficheiro in ficheiros:
                file_url = quote(ficheiro) # Trata nomes com espaços ou caracteres especiais
                
                # Construção do Link Externo
                if categoria == 'video' and ficheiro in LINKS_VIDEOS:
                    link_externo = LINKS_VIDEOS[ficheiro]
                else:
                    # AQUI: Ajustado para o teu caminho: thephotosintese/fotografia/nome-da-pasta/foto.jpg
                    link_externo = f"{cloudinary_base}/thephotosintese/fotografia/{subcategoria}/{file_url}"
                
                # --- Lógica da Legenda ---
                # 1. Procura no JSON
                # 2. Se não existir, gera o nome automático baseado no ficheiro
                titulo_default = os.path.splitext(ficheiro)[0].replace('-', ' ').replace('_', ' ').title()
                titulo_final = legendas_da_pasta.get(ficheiro, titulo_default)

                # --- Poster para Vídeos ---
                poster_url = CAPAS_VIDEOS.get(ficheiro) 
                if categoria == 'video' and not poster_url:
                    if "cloudinary.com" in link_externo:
                        # Gera uma thumbnail automática do Cloudinary
                        base_link = link_externo.rsplit('.', 1)[0] + '.jpg'
                        poster_url = base_link.replace('/video/upload/', '/video/upload/f_auto,q_auto,so_auto,w_800/')

                itens.append({
                    'titulo': titulo_final,
                    'imagem': link_externo,
                    'poster': poster_url  
                })

        except Exception as e:
            print(f"[DEBUG] Erro ao processar ficheiros: {e}")
    else:
        print(f"[DEBUG] Pasta local não encontrada: {path}")
    
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