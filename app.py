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
    'festas de aniversário': 'festadeanos.jpg',
    'espetáculos': 'espet.jpg',
    'eventos corporativos': 'corporativo.jpg',
    'sessões fotográficas': 'sessoesfoto.jpg',
    'os-casamentos': 'wedvideo.jpg',
    'os-baptizados': 'bapvideo.jpg',
    'os-concertos-e-espetáculos': 'showsvideo.jpg'
}

# Links para vídeos no Cloudinary
LINKS_VIDEOS = {
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282255/AnabelaRui.mp4',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282236/AnaJoao.mp4',
    'PatriciaDiogo.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282235/PatriciaDiogo.mp4',
    'JuniorVivianne.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773282245/JuniorVivianne.mp4',
    'Hairspray.mp4': 'https://res.cloudinary.com/dilatofg5/video/upload/v1773784540/Hairspray.mp4'
}

# Poster/Capa dos vídeos
CAPAS_VIDEOS = {
    'AnabelaRui.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400674/Anabela_e_Rui.png',
    'AnaJoao.mp4': 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400693/anaejoao.jpg',
    'VivianeJunior.mp4' : 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400856/vivianejunior.jpg' ,
    'PatriciaDiogo.mp4' : 'https://res.cloudinary.com/dilatofg5/image/upload/f_auto,q_auto,w_1200/v1773400855/catarinadiogo.jpg',
    'Hairspray.mp4' : 'https://res.cloudinary.com/dilatofg5/image/upload/v1773785190/Untitled-1.jpg'
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
    # URLs base do Cloudinary (Sem o v1741... para evitar erros de cache)
    CLOUDINARY_BASE_IMG = "https://res.cloudinary.com/dilatofg5/image/upload"
    CLOUDINARY_BASE_VID = "https://res.cloudinary.com/dilatofg5/video/upload"
    
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
                    cloudinary_base = CLOUDINARY_BASE_VID if categoria == 'video' else CLOUDINARY_BASE_IMG
                    
                    # --- CONFIGURAÇÃO DO CAMINHO (MUITO IMPORTANTE) ---
                    # Se no Cloudinary as fotos estão na RAIZ (como o teu exemplo), usa isto:
                    link_externo = f"{cloudinary_base}/{file_url}"
                    
                    # SE decidires usar pastas no Cloudinary, o link deve ser:
                    # link_externo = f"{cloudinary_base}/thephotosintese/fotografia/{subcategoria}/{file_url}"
                
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