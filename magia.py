import os

# As pastas onde estão os teus ficheiros pesados
pastas_alvo = ['static/assets/img', 'static/assets/videos']
extensoes_pesadas = ('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.webm')

print("A iniciar a transformação em fantasmas...")

for pasta in pastas_alvo:
    if os.path.exists(pasta):
        for root, dirs, files in os.walk(pasta):
            for file in files:
                if file.lower().endswith(extensoes_pesadas):
                    caminho_completo = os.path.join(root, file)
                    
                    # Abre o ficheiro e apaga tudo o que está lá dentro (fica com 0 bytes)
                    with open(caminho_completo, 'w') as f:
                        pass
                    
                    print(f"Fantasma criado: {file}")

print("Feito! Todos os ficheiros têm agora 0 bytes. O teu projeto está super leve!")