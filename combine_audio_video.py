#!/usr/bin/env python3
"""
Script para combinar um áudio com um vídeo existente.
"""
import os
import sys
import argparse
from datetime import datetime
import moviepy.editor as mp

def combine_audio_video(video_path, audio_path, output_path=None):
    """
    Combina um áudio com um vídeo existente.
    
    Args:
        video_path (str): Caminho para o vídeo.
        audio_path (str): Caminho para o áudio.
        output_path (str, optional): Caminho para o vídeo de saída.
        
    Returns:
        str: Caminho para o vídeo de saída.
    """
    try:
        # Verificar se os arquivos existem
        if not os.path.exists(video_path):
            print(f"Erro: Vídeo não encontrado: {video_path}")
            return None
            
        if not os.path.exists(audio_path):
            print(f"Erro: Áudio não encontrado: {audio_path}")
            return None
            
        # Gerar nome de arquivo baseado no timestamp se não for fornecido
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = os.path.join(os.getcwd(), "output", "videos")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"rapidinha_combined_{timestamp}.mp4")
            
        # Carregar o vídeo e o áudio
        print(f"Carregando vídeo: {video_path}")
        video = mp.VideoFileClip(video_path)
        
        print(f"Carregando áudio: {audio_path}")
        audio = mp.AudioFileClip(audio_path)
        
        # Ajustar a duração do vídeo para corresponder ao áudio
        if video.duration > audio.duration:
            print(f"Ajustando duração do vídeo para corresponder ao áudio: {audio.duration:.2f} segundos")
            video = video.subclip(0, audio.duration)
        elif video.duration < audio.duration:
            print(f"Aviso: O áudio é mais longo que o vídeo. Apenas {video.duration:.2f} segundos do áudio serão usados.")
            audio = audio.subclip(0, video.duration)
            
        # Combinar o vídeo com o áudio
        print("Combinando vídeo e áudio...")
        final_video = video.set_audio(audio)
        
        # Salvar o vídeo final
        print(f"Salvando vídeo final: {output_path}")
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # Fechar os clips
        video.close()
        audio.close()
        final_video.close()
        
        print(f"Vídeo combinado com sucesso: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Erro ao combinar áudio e vídeo: {e}")
        return None

def main():
    """
    Função principal.
    """
    parser = argparse.ArgumentParser(description="Combina um áudio com um vídeo existente.")
    parser.add_argument("--video", required=True, help="Caminho para o vídeo")
    parser.add_argument("--audio", required=True, help="Caminho para o áudio")
    parser.add_argument("--output", help="Caminho para o vídeo de saída")
    
    args = parser.parse_args()
    
    combine_audio_video(args.video, args.audio, args.output)

if __name__ == "__main__":
    main()
