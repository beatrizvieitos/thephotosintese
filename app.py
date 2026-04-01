import os
import json
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
    'os-baptizados': 'bapvideo.jpg',
    'os-concertos-e-espetáculos': 'showsvideo.jpg'
}

# Links para vídeos no ImageKit (assumindo que estão na pasta videos/os-casamentos)
LINKS_VIDEOS = {
    'AnabelaRui.mp4': 'tgFrktZ4_hg',
    'AnaJoao.mp4': 'wdXenml1LeI',
    'PatriciaDiogo.mp4': 'syb3rxrscdg',
    'VivianeJunior.mp4': 'Y4Egto0Mseg',
    'ClaudiaHugo.mp4': 'QXqN4qMGkDc',
    'Hairspray.mp4': 'LksyvlTTBWQ',
    'MarilynOMusical.mp4': 'B-y_w6TGdl4',
    'CriadoresTikTok.mp4': '3eYrPMymEIg',
    'Alyssa.mp4': 'I3VV0XRRRvc'
}

# Poster/Capa dos vídeos
CAPAS_VIDEOS = {
    'AnabelaRui.mp4': 'https://ik.imagekit.io/bvm99/anabelarui.png',
    'AnaJoao.mp4': 'https://ik.imagekit.io/bvm99/anaejoao.jpg',
    'VivianeJunior.mp4' : 'https://ik.imagekit.io/bvm99/vivianeejunior.jpg' ,
    'PatriciaDiogo.mp4' : 'https://ik.imagekit.io/bvm99/patriciadiogo.jpg',
    'ClaudiaHugo.mp4' : 'https://ik.imagekit.io/bvm99/claudiahugo.jpg',
    'Hairspray.mp4' : 'https://ik.imagekit.io/bvm99/hairspray.jpg',
    'MarilynOMusical.mp4' : 'https://ik.imagekit.io/bvm99/marilynomusical.jpg',
    'CriadoresTikTok.mp4' : 'https://ik.imagekit.io/bvm99/criadorestiktok.jpg'
}

# Função para carregar legendas do ficheiro externo
def carregar_legendas():
    try:
        with open('legendas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio/<categoria>')
def menu_categorias(categoria):
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
    IMAGEKIT_BASE_IMG = "https://ik.imagekit.io/bvm99/tr:w-1200"
    IMAGEKIT_BASE_VID = "https://ik.imagekit.io/bvm99/tr:f-mp4"
    
    base_folder = IMAGE_FOLDER if categoria == 'fotografia' else VIDEO_FOLDER
    path = os.path.join(base_folder, subcategoria)
    itens = []
    
    # Carregar as legendas do JSON externo
    todas_as_legendas = carregar_legendas()
    legendas_da_pasta = todas_as_legendas.get(subcategoria, {})
    
    if os.path.exists(path):
        try:
            ficheiros = os.listdir(path)
            # Filtro de extensões (Imagens e Vídeos)
            ficheiros = [f for f in ficheiros if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4'))]
            ficheiros.sort()
            
            for ficheiro in ficheiros:
                file_url = quote(ficheiro)
                
                if categoria == 'video' and ficheiro in LINKS_VIDEOS:
                    link_externo = LINKS_VIDEOS[ficheiro]
                else:
                    cloudinary_base = IMAGEKIT_BASE_VID if categoria == 'video' else IMAGEKIT_BASE_IMG
                    
                    # --- CONFIGURAÇÃO DO CAMINHO ---
                    if categoria == 'video':
                        # Vai buscar o ID do YouTube correspondente ao nome do ficheiro
                        link_externo = YOUTUBE_VIDEOS.get(ficheiro, '') 
                    else:
                        # As fotos continuam a vir do ImageKit normalmente!
                        link_externo = f"{IMAGEKIT_BASE_IMG}/fotos/{subcategoria}/{file_url}"
                
                # --- LEGENDA ---
                # Procura no JSON; se não existir, limpa o nome do ficheiro automaticamente
                titulo_default = os.path.splitext(ficheiro)[0].replace('-', ' ').replace('_', ' ').title()
                titulo_final = legendas_da_pasta.get(ficheiro, titulo_default)

                itens.append({
                    'titulo': titulo_final,
                    'imagem': link_externo,
                    'poster': CAPAS_VIDEOS.get(ficheiro)
                })

        except Exception as e:
            print(f"[DEBUG] Erro: {e}")
            
    return render_template('portfolioFoto.html', categoria=categoria, subcategoria=subcategoria, itens=itens, tipo=categoria)



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

if __name__ == '__main__':
    app.run(debug=True)