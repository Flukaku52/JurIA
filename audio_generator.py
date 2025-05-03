"""
Módulo para gerar áudio a partir de texto usando a API da ElevenLabs.
"""
import os
import json
import time
import requests
from dotenv import load_dotenv
import elevenlabs

# Carregar variáveis de ambiente
load_dotenv()

class AudioGenerator:
    """
    Classe para gerar áudio a partir de texto usando a API da ElevenLabs.
    """

    def __init__(self):
        """
        Inicializa o gerador de áudio.
        """
        # Chave da API ElevenLabs
        self.api_key = os.getenv("ELEVENLABS_API_KEY")

        # Se não conseguir obter a chave do ambiente, tentar ler diretamente do arquivo .env
        if not self.api_key:
            try:
                with open('.env', 'r') as f:
                    for line in f:
                        if line.startswith('ELEVENLABS_API_KEY='):
                            self.api_key = line.strip().split('=', 1)[1]
                            break
            except Exception as e:
                print(f"Erro ao ler arquivo .env: {e}")

        if not self.api_key:
            print("Aviso: API key da ElevenLabs não encontrada. A geração de áudio não funcionará.")
        else:
            print(f"API key da ElevenLabs encontrada: {self.api_key[:5]}...{self.api_key[-5:]}")

        # Diretório para armazenar os áudios gerados
        self.audio_dir = os.path.join(os.getcwd(), "output", "audio")
        os.makedirs(self.audio_dir, exist_ok=True)

        # Configurações de voz
        self.voice_settings = {
            "stability": 0.15,          # Estabilidade mínima para capturar o chiado carioca nos 's' finais
            "similarity_boost": 1.0,     # Máxima similaridade possível com a voz original
            "style": 1.0,               # Máximo estilo possível para capturar a entonação carioca
            "use_speaker_boost": True,   # Melhorar a qualidade do áudio
            "model_id": "eleven_multilingual_v2"  # Modelo multilíngue avançado para melhor sotaque
        }

        # Carregar configuração da voz se existir
        self.voice_id = None
        self.voice_name = "Rapidinha Voice"
        self._load_voice_config()

    def _load_voice_config(self):
        """
        Carrega a configuração da voz de um arquivo.
        """
        config_path = os.path.join(os.getcwd(), "config", "voice_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.voice_id = config.get("voice_id")
                    self.voice_name = config.get("voice_name", "Rapidinha Voice")

                    # Carregar configurações avançadas se disponíveis
                    if "settings" in config:
                        self.voice_settings.update(config["settings"])
                        print(f"Configurações avançadas carregadas: {self.voice_settings}")

                    print(f"Configuração de voz carregada. ID: {self.voice_id}, Nome: {self.voice_name}")
            except Exception as e:
                print(f"Erro ao carregar configuração de voz: {e}")

    def generate_audio(self, text, output_path=None):
        """
        Gera áudio a partir de texto usando a API da ElevenLabs.

        Args:
            text (str): Texto a ser convertido em áudio.
            output_path (str, optional): Caminho para salvar o arquivo de áudio. Se None, gera um nome baseado no timestamp.

        Returns:
            str: Caminho para o arquivo de áudio gerado, ou None se falhar.
        """
        if not self.api_key:
            print("API key da ElevenLabs não configurada. Não é possível gerar áudio.")
            return None

        try:
            # Gerar nome de arquivo baseado no timestamp se não for fornecido
            if not output_path:
                timestamp = int(time.time())
                output_path = os.path.join(self.audio_dir, f"audio_{timestamp}.mp3")

            # Verificar se temos uma voz configurada
            voice_identifier = self.voice_id if self.voice_id else "Rachel"

            # Preparar a requisição para a API
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_identifier}"

            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }

            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",  # Modelo multilíngue avançado para melhor sotaque
                "voice_settings": self.voice_settings
            }

            # Fazer a requisição para a API
            print(f"Gerando áudio para o texto: '{text[:50]}...'")
            response = requests.post(url, json=data, headers=headers, timeout=60)
            response.raise_for_status()

            # Salvar o áudio
            with open(output_path, 'wb') as f:
                f.write(response.content)

            print(f"Áudio gerado com sucesso: {output_path}")
            return output_path

        except Exception as e:
            print(f"Erro ao gerar áudio: {e}")
            return None

    def clone_voice(self, audio_files, voice_name="Rapidinha Voice"):
        """
        Clona uma voz a partir de arquivos de áudio.

        Args:
            audio_files (list): Lista de caminhos para arquivos de áudio.
            voice_name (str): Nome da voz a ser criada.

        Returns:
            str: ID da voz clonada, ou None se falhar.
        """
        if not self.api_key:
            print("API key da ElevenLabs não configurada. Não é possível clonar voz.")
            return None

        try:
            # Verificar se temos arquivos de áudio válidos
            valid_files = []
            for audio_file in audio_files:
                if os.path.exists(audio_file):
                    valid_files.append(audio_file)

            if not valid_files:
                print("Nenhum arquivo de áudio válido encontrado.")
                return None

            # Clonar a voz usando a API da ElevenLabs
            print(f"Clonando voz a partir de {len(valid_files)} arquivos de áudio...")

            # Preparar os arquivos para upload
            files = []
            for audio_file in valid_files:
                with open(audio_file, 'rb') as f:
                    files.append(('files', (os.path.basename(audio_file), f.read(), 'audio/mpeg')))

            # Fazer a requisição para a API
            import requests
            url = "https://api.elevenlabs.io/v1/voices/add"
            headers = {"xi-api-key": self.api_key}
            data = {
                "name": voice_name,
                "description": "Voz clonada para o quadro Rapidinha no Cripto"
            }

            response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()

            # Processar a resposta
            result = response.json()
            voice_id = result.get("voice_id")

            if voice_id:
                print(f"Voz clonada com sucesso! ID: {voice_id}")

                # Atualizar o ID da voz
                self.voice_id = voice_id
                self.voice_name = voice_name

                # Salvar o ID da voz e configurações avançadas em um arquivo de configuração
                config_path = os.path.join(os.getcwd(), "config", "voice_config.json")
                os.makedirs(os.path.dirname(config_path), exist_ok=True)

                # Configurações avançadas para o sotaque carioca
                voice_config = {
                    "voice_id": voice_id,
                    "voice_name": voice_name,
                    "settings": {
                        "stability": 0.15,
                        "similarity_boost": 1.0,
                        "style": 1.0,
                        "use_speaker_boost": True,
                        "model_id": "eleven_multilingual_v2"
                    }
                }

                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(voice_config, f, ensure_ascii=False, indent=4)

                return voice_id
            else:
                print("Falha ao clonar voz. Nenhum ID de voz retornado.")
                return None

        except Exception as e:
            print(f"Erro ao clonar voz: {e}")
            return None

    def extract_audio_samples(self, video_dir, max_samples=5, max_duration=30):
        """
        Extrai amostras de áudio de vídeos para clonagem de voz.

        Args:
            video_dir (str): Diretório contendo os vídeos.
            max_samples (int): Número máximo de amostras a extrair.
            max_duration (int): Duração máxima de cada amostra em segundos.

        Returns:
            list: Lista de caminhos para os arquivos de áudio extraídos.
        """
        try:
            import moviepy.editor as mp

            # Diretório para armazenar as amostras
            samples_dir = os.path.join(os.getcwd(), "reference", "voice_samples")
            os.makedirs(samples_dir, exist_ok=True)

            # Listar todos os vídeos no diretório
            video_files = []
            for filename in os.listdir(video_dir):
                if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_files.append(os.path.join(video_dir, filename))

            if not video_files:
                print("Nenhum vídeo encontrado no diretório.")
                return []

            # Limitar o número de vídeos
            video_files = video_files[:max_samples]

            # Extrair amostras de áudio
            audio_samples = []
            for i, video_file in enumerate(video_files):
                try:
                    # Extrair áudio do vídeo
                    video = mp.VideoFileClip(video_file)

                    # Limitar a duração
                    if video.duration > max_duration:
                        video = video.subclip(0, max_duration)

                    # Salvar o áudio
                    audio_path = os.path.join(samples_dir, f"sample_{i+1}.mp3")
                    video.audio.write_audiofile(audio_path, codec='mp3')

                    # Adicionar à lista de amostras
                    audio_samples.append(audio_path)

                    # Fechar o vídeo
                    video.close()

                except Exception as e:
                    print(f"Erro ao extrair áudio do vídeo {video_file}: {e}")

            print(f"Extraídas {len(audio_samples)} amostras de áudio para clonagem de voz.")
            return audio_samples

        except ImportError:
            print("Erro: biblioteca moviepy não encontrada. Instale moviepy.")
            return []
        except Exception as e:
            print(f"Erro ao extrair amostras de áudio: {e}")
            return []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerador de áudio para o Clone Rapidinha no Cripto")
    parser.add_argument("--text", help="Texto a ser convertido em áudio")
    parser.add_argument("--clone", action="store_true", help="Clonar voz a partir de amostras de áudio")
    parser.add_argument("--extract", action="store_true", help="Extrair amostras de áudio de vídeos")
    parser.add_argument("--list-voices", action="store_true", help="Listar vozes disponíveis")
    parser.add_argument("--play", action="store_true", help="Reproduzir o áudio gerado")

    args = parser.parse_args()

    generator = AudioGenerator()

    if args.list_voices:
        try:
            print("Vozes disponíveis:")
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": generator.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            voices_data = response.json()

            for voice in voices_data.get("voices", []):
                print(f"- {voice.get('name')} (ID: {voice.get('voice_id')})")
        except Exception as e:
            print(f"Erro ao listar vozes: {e}")

    if args.extract:
        video_dir = os.path.join(os.getcwd(), "reference", "videos")
        generator.extract_audio_samples(video_dir)

    if args.clone:
        samples_dir = os.path.join(os.getcwd(), "reference", "voice_samples")
        if os.path.exists(samples_dir):
            audio_files = [os.path.join(samples_dir, f) for f in os.listdir(samples_dir) if f.endswith('.mp3')]
            if audio_files:
                generator.clone_voice(audio_files)
            else:
                print("Nenhuma amostra de áudio encontrada. Execute primeiro com --extract.")
        else:
            print("Diretório de amostras não encontrado. Execute primeiro com --extract.")

    if args.text:
        audio_path = generator.generate_audio(args.text)
        if audio_path and args.play:
            try:
                # Reproduzir o áudio usando o player padrão do sistema
                import subprocess
                import platform

                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.call(["afplay", audio_path])
                elif system == "Windows":
                    subprocess.call(["start", audio_path], shell=True)
                else:  # Linux e outros
                    subprocess.call(["xdg-open", audio_path])
            except Exception as e:
                print(f"Erro ao reproduzir áudio: {e}")
