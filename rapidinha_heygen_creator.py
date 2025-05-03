#!/usr/bin/env python3
"""
Criador de vídeos para o quadro "Rapidinha Cripto" usando o HeyGen
"""
import os
import argparse
import sys
from datetime import datetime
from rapidinha_generator_ai import RapidinhaCryptoGenerator
from audio_generator import AudioGenerator
from heygen_video_generator import HeyGenVideoGenerator

def create_rapidinha_video(args):
    """
    Cria um vídeo completo para o quadro "Rapidinha Cripto" usando o HeyGen.

    Args:
        args: Argumentos da linha de comando.
    """
    print("\n=== Criando vídeo para 'Rapidinha Cripto' com HeyGen ===")

    # Criar diretórios de saída
    output_dir = os.path.join(os.getcwd(), "output")
    audio_dir = os.path.join(output_dir, "audio")
    video_dir = os.path.join(output_dir, "videos")

    for directory in [output_dir, audio_dir, video_dir]:
        os.makedirs(directory, exist_ok=True)

    # Etapa 1: Gerar o script
    print("\n--- Etapa 1: Gerando script ---")
    try:
        generator = RapidinhaCryptoGenerator()

        # Gerar o script com as opções especificadas
        script_path = generator.create_rapidinha(
            use_real_news=not args.mock,
            use_ai=not args.no_ai
        )

        print(f"Script gerado com sucesso: {script_path}")

        # Exibir o script
        with open(script_path, 'r', encoding='utf-8') as file:
            script_content = file.read()
            print("\n" + "="*50 + "\n")
            print(script_content)
            print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Erro ao gerar o script: {e}")
        return

    # Etapa 2: Gerar o áudio
    print("\n--- Etapa 2: Gerando áudio ---")
    try:
        audio_generator = AudioGenerator()

        # Gerar nome para o arquivo de áudio
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = os.path.join(audio_dir, f"rapidinha_audio_{timestamp}.mp3")

        # Gerar o áudio
        audio_path = audio_generator.generate_audio(script_content, audio_path)

        if not audio_path:
            print("Falha ao gerar áudio. Continuando sem áudio...")
    except Exception as e:
        print(f"Erro ao gerar o áudio: {e}")
        audio_path = None

    # Etapa 3: Gerar o vídeo com o HeyGen
    print("\n--- Etapa 3: Gerando vídeo com HeyGen ---")
    try:
        heygen_generator = HeyGenVideoGenerator()

        # Usar seu avatar personalizado
        heygen_generator.avatar_id = "3228e777071e48e887d7a9bb5066d921"  # Vídeo do WhatsApp
        print(f"Usando seu avatar personalizado: {heygen_generator.avatar_id}")

        # Gerar nome para o arquivo de vídeo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_path = os.path.join(video_dir, f"rapidinha_heygen_{timestamp}.mp4")

        # Gerar o vídeo
        video_path = heygen_generator.generate_video(script_content, audio_path, video_path)

        if video_path:
            print(f"\nVídeo gerado com sucesso: {video_path}")
        else:
            print("\nFalha ao gerar o vídeo.")
    except Exception as e:
        print(f"Erro ao gerar o vídeo: {e}")

def setup_avatar(args):
    """
    Configura o avatar para o HeyGen.

    Args:
        args: Argumentos da linha de comando.
    """
    print("\n=== Configurando avatar para o HeyGen ===")

    try:
        heygen_generator = HeyGenVideoGenerator()

        if args.list:
            # Listar avatares disponíveis
            heygen_generator.list_avatars()
        elif args.create and args.video:
            # Criar um novo avatar
            avatar_name = args.name if args.name else "Rapidinha Avatar"
            heygen_generator.create_avatar_from_video(args.video, avatar_name)
        else:
            print("Erro: Você deve especificar --list para listar avatares ou --create --video CAMINHO_DO_VIDEO para criar um novo avatar.")
    except Exception as e:
        print(f"Erro ao configurar avatar: {e}")

def list_videos():
    """
    Lista os vídeos gerados anteriormente.
    """
    videos_dir = os.path.join(os.getcwd(), "output", "videos")
    if not os.path.exists(videos_dir):
        print("\nDiretório de vídeos não encontrado.")
        return

    videos = [
        f for f in os.listdir(videos_dir)
        if f.startswith("rapidinha_heygen_") and f.endswith(".mp4")
    ]

    if not videos:
        print("\nNenhum vídeo do HeyGen encontrado.")
        return

    print("\nVídeos do HeyGen gerados anteriormente:")
    for i, video in enumerate(sorted(videos, reverse=True), 1):
        # Extrair data e hora do nome do arquivo
        date_str = video.replace("rapidinha_heygen_", "").replace(".mp4", "")
        try:
            date_obj = datetime.strptime(date_str, "%Y%m%d_%H%M%S")
            formatted_date = date_obj.strftime("%d/%m/%Y às %H:%M:%S")
        except:
            formatted_date = date_str

        video_path = os.path.join(videos_dir, video)
        size_mb = os.path.getsize(video_path) / (1024 * 1024)

        print(f"{i}. {formatted_date} - {video_path} ({size_mb:.2f} MB)")

def main():
    """
    Função principal que coordena o fluxo da aplicação.
    """
    parser = argparse.ArgumentParser(
        description="Criador de vídeos para o quadro 'Rapidinha Cripto' usando o HeyGen",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando para criar vídeo
    create_parser = subparsers.add_parser("create", help="Criar um novo vídeo")
    create_parser.add_argument(
        "--mock",
        action="store_true",
        help="Usar notícias simuladas em vez de notícias reais"
    )
    create_parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Não usar IA para gerar explicações"
    )
    create_parser.add_argument(
        "--video",
        help="Caminho para um vídeo de referência para criar um novo avatar"
    )

    # Comando para configurar avatar
    avatar_parser = subparsers.add_parser("avatar", help="Configurar avatar para o HeyGen")
    avatar_parser.add_argument(
        "--list",
        action="store_true",
        help="Listar avatares disponíveis"
    )
    avatar_parser.add_argument(
        "--create",
        action="store_true",
        help="Criar um novo avatar"
    )
    avatar_parser.add_argument(
        "--video",
        help="Caminho para um vídeo de referência para criar um novo avatar"
    )
    avatar_parser.add_argument(
        "--name",
        default="Rapidinha Avatar",
        help="Nome do avatar a ser criado (padrão: 'Rapidinha Avatar')"
    )

    # Comando para listar vídeos
    subparsers.add_parser("list", help="Listar vídeos gerados anteriormente")

    # Se nenhum argumento for fornecido, mostrar ajuda
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # Executar a ação correspondente ao comando fornecido
    if args.command == "create":
        create_rapidinha_video(args)
    elif args.command == "avatar":
        setup_avatar(args)
    elif args.command == "list":
        list_videos()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
