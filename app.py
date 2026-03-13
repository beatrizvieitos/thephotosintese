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
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/v1741643231/Anabela_e_Rui_poster.png',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/v1741643231/anaejoao_poster.jpg',
    'PatriciaDiogo.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/v1741643231/Patricia_e_Diogo_poster.jpg',
    'JuniorVivianne.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/v1741643231/vivianeejunior_poster.jpg'
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
    """Mostra a grelha de fotos ou vídeos da subcategoria (via Cloudinary)"""
    
    # Base URLs para o Cloudinary
    CLOUDINARY_BASE_IMG = "https://res.cloudinary.com/dilatofg5/image/upload/v1741643231"
    CLOUDINARY_BASE_VID = "https://res.cloudinary.com/dilatofg5/video/upload/v1741643231"
    
    # Pasta base dependendo da categoria
    base_folder = IMAGE_FOLDER if categoria == 'fotografia' else VIDEO_FOLDER
    
    # Caminho completo para a subcategoria local (usado apenas para saber que ficheiros existem)
    path = os.path.join(base_folder, subcategoria)
    
    itens = []
    
    # Um pequeno dicionário opcional se quiser dar títulos mais bonitos aos ficheiros
    legendas = {
        'FOTO-232.jpg': 'Momento Especial',
        'PHOTO-423.jpg': 'A Cerimónia',
        'AnaJoao.mp4': 'O Casamento da Ana e do João',
        'AnabelaRui.mp4': 'A Celebração da Anabela e do Rui'
    }
    
    if os.path.exists(path):
        try:
            ficheiros = os.listdir(path)
            
            # Filtra apenas imagens/vídeos
            if categoria == 'video':
                ficheiros = [f for f in ficheiros if f.lower().endswith(('.mp4', '.mov', '.webm'))]
                cloudinary_base = CLOUDINARY_BASE_VID
            else:
                ficheiros = [f for f in ficheiros if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                cloudinary_base = CLOUDINARY_BASE_IMG
            
            # Ordena os ficheiros
            ficheiros.sort()
            
            for ficheiro in ficheiros:
                if categoria == 'video' and ficheiro in LINKS_VIDEOS:
                    # Usa o link direto configurado
                    link_externo = LINKS_VIDEOS[ficheiro]
                else:
                    file_url = quote(ficheiro)
                    
                    # -------------------------------------------------------------
                    # SOLUÇÃO CLOUDINARY:
                    # Atualmente, o seu código constrói o link para a RAIZ do Cloudinary:
                    link_externo = f"{cloudinary_base}/{file_url}"
                    
                    # Se no Cloudinary você guardou as fotos dentro de uma pasta (ex: "casamentos"), 
                    # então comente a linha acima (com um #) e tire o # da linha abaixo:
                    # link_externo = f"{cloudinary_base}/{quote(subcategoria)}/{file_url}"
                    # -------------------------------------------------------------
                
                # Título a partir do nome do ficheiro (remove extensão)
                titulo = os.path.splitext(ficheiro)[0].replace('-', ' ').replace('_', ' ').title()
                
                itens.append({
                    'titulo': legendas.get(ficheiro, titulo),
                    'imagem': link_externo,
                    'poster': CAPAS_VIDEOS.get(ficheiro, None)  # Para vídeos com poster
                })
        except Exception as e:
            print(f"[DEBUG] Erro a ler directório: {e}", flush=True)
    else:
        print(f"[DEBUG] ERRO: Pasta não encontrada: {path}", flush=True)
    
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