import instaloader
from pydub import AudioSegment
import whisper
import os
import glob

# Função para baixar o vídeo do Instagram e retornar o caminho real do arquivo
def download_instagram_video(url):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    
    # Define o diretório de destino
    target_dir = "video"
    os.makedirs(target_dir, exist_ok=True)
    
    # Baixa o post
    L.download_post(post, target=target_dir)
    
    # Encontra o arquivo de vídeo baixado (pode ser .mp4 ou outro formato)
    video_files = glob.glob(os.path.join(target_dir, "*.mp4"))  # Procura por arquivos MP4
    
    if not video_files:
        raise FileNotFoundError("Nenhum arquivo de vídeo foi baixado.")
    
    return video_files[0]  # Retorna o primeiro arquivo de vídeo encontrado

# Função para extrair o áudio do vídeo
def extract_audio_from_video(video_path, audio_path="audio.wav"):
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format="wav")
    return audio_path

# Função para transcrever o áudio usando Whisper local
def transcribe_audio(audio_path, model="base"):
    print("Carregando o modelo Whisper...")
    model = whisper.load_model(model)
    result = model.transcribe(audio_path)
    return result["text"]

# Função principal
def main():
    try:
        # Solicitar a URL do Instagram ao usuário
        url = input("Por favor, insira a URL do post do Instagram: ")
        
        # Baixar o vídeo
        print("Baixando o vídeo...")
        video_path = download_instagram_video(url)
        print(f"Vídeo baixado: {video_path}")
        
        # Extrair o áudio
        print("Extraindo o áudio do vídeo...")
        audio_path = extract_audio_from_video(video_path)
        
        # Transcrever o áudio
        print("Transcrevendo o áudio...")
        transcript = transcribe_audio(audio_path)
        
        # Exibir e salvar a transcrição
        print("\nTranscrição do vídeo:")
        print(transcript)
        
        with open("transcricao.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        print("\nTranscrição salva em 'transcricao.txt'.")
        
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    finally:
        # Limpar arquivos temporários (opcional)
        if 'video_path' in locals() and os.path.exists(video_path):
            os.remove(video_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
        print("Processo concluído.")

if __name__ == "__main__":
    main()