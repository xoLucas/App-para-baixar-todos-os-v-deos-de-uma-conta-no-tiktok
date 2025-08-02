# backend_app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import shutil

app = Flask(__name__)
CORS(app)

# Diretório onde os vídeos baixados serão temporariamente armazenados
DOWNLOAD_FOLDER = 'downloaded_videos'
# Cria o diretório se ele não existir
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Define o caminho completo para o executável yt-dlp.
YT_DLP_EXECUTABLE = 'C:\\Users\\lucas\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\yt-dlp.exe'

# --- NOVIDADE: Configuração de Cookies ---
# Você precisará colar o conteúdo do arquivo de cookies exportado aqui.
# Para fins de segurança e praticidade, é melhor usar um arquivo de cookies.
# Se você exportou para um arquivo 'cookies.txt' (formato Netscape),
# coloque-o na mesma pasta do backend_app.py e defina:
COOKIES_FILE = 'cookies.txt' # Nome do arquivo de cookies
# Se você não quiser usar um arquivo e preferir colar o conteúdo JSON diretamente,
# isso é mais complexo e menos recomendado devido à formatação.
# Para este exemplo, vamos usar a abordagem de arquivo de cookies.
# --- FIM DA NOVIDADE ---


@app.route('/api/download-tiktok-profile', methods=['POST'])
def download_tiktok_profile():
    """
    Endpoint para baixar vídeos de um perfil do TikTok.
    Recebe o link do perfil via POST e usa yt-dlp para baixar os vídeos.
    """
    data = request.get_json()
    tiktok_link = data.get('link')

    if not tiktok_link:
        return jsonify({"success": False, "message": "Link do TikTok não fornecido."}), 400

    if not tiktok_link.startswith('https://www.tiktok.com/@'):
        return jsonify({"success": False, "message": "Link inválido. Por favor, use um link de perfil do TikTok válido."}), 400

    # Cria um subdiretório para cada perfil para organizar os downloads
    try:
        username = tiktok_link.split('@')[1].split('?')[0].split('/')[0]
        profile_download_path = os.path.join(DOWNLOAD_FOLDER, username)
        if not os.path.exists(profile_download_path):
            os.makedirs(profile_download_path)
    except IndexError:
        return jsonify({"success": False, "message": "Não foi possível extrair o nome de usuário do link."}), 400

    # Verifica se o arquivo de cookies existe
    cookies_filepath = os.path.join(os.path.dirname(__file__), COOKIES_FILE)
    if not os.path.exists(cookies_filepath):
        return jsonify({"success": False, "message": f"Erro: Arquivo de cookies '{COOKIES_FILE}' não encontrado. Por favor, crie este arquivo na mesma pasta do backend_app.py e cole seus cookies do TikTok nele."}), 500

    try:
        # Comando yt-dlp para baixar todos os vídeos de um perfil
        # Adicionado a opção '--cookies' para passar o arquivo de cookies
        command = [
            YT_DLP_EXECUTABLE,
            tiktok_link,
            '--yes-playlist',
            '--cookies', cookies_filepath, # <--- NOVIDADE: Passando o arquivo de cookies
            '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            '--merge-output-format', 'mp4',
            '--restrict-filenames',
            '--no-warnings',
            '--ignore-errors',
            '-o', os.path.join(profile_download_path, '%(upload_date)s-%(id)s-%(title)s.%(ext)s')
        ]

        # Executa o comando yt-dlp
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print("yt-dlp stdout:", result.stdout)
        print("yt-dlp stderr:", result.stderr)

        return jsonify({"success": True, "message": f"Download dos vídeos de '{username}' iniciado no servidor. Verifique a pasta '{profile_download_path}'."}), 200

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar yt-dlp: {e.stderr}")
        return jsonify({"success": False, "message": f"Erro ao baixar vídeos: {e.stderr.strip()}"}), 500
    except FileNotFoundError:
        return jsonify({"success": False, "message": f"Erro: yt-dlp não encontrado no caminho especificado: {YT_DLP_EXECUTABLE}. Certifique-se de que o caminho está correto e o arquivo existe."}), 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({"success": False, "message": f"Ocorreu um erro inesperado: {str(e)}"}), 500

@app.route('/api/cleanup_downloads', methods=['POST'])
def cleanup_downloads():
    """Endpoint para limpar o diretório de downloads."""
    try:
        if os.path.exists(DOWNLOAD_FOLDER):
            shutil.rmtree(DOWNLOAD_FOLDER)
            os.makedirs(DOWNLOAD_FOLDER)
        return jsonify({"success": True, "message": "Diretório de downloads limpo com sucesso."}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao limpar downloads: {str(e)}"}), 500

@app.route('/')
def home():
    """
    Endpoint de demonstração para a raiz do servidor.
    Em um ambiente real, você serviria seu arquivo index.html aqui.
    """
    return "O backend do Baixador de Vídeos do TikTok está rodando!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

