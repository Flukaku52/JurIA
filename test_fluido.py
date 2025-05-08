#!/usr/bin/env python3
"""
Script para testar a fluidez da fala sem gastar créditos.
"""
import os
import sys
import json
from datetime import datetime

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.text import TextProcessor
from core.utils import ensure_directory, PROJECT_ROOT, OUTPUT_DIR

# Texto de entrada
input_text = """E aí cambada, tô de volta na área e bora de Rapidinha! Mas dessa vez eu tenho um desafio pra vocês, tem algo "diferente" nesse vídeo, você consegue adivinhar o que? Bota aí nos comentários pra ver se você acerta, no fim do vídeo eu dou a resposta!"""

# Diretórios
text_dir = os.path.join(OUTPUT_DIR, "text")
ensure_directory(text_dir)

# Timestamp para os arquivos
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
base_filename = f"fluido_{timestamp}"

# Criar processador de texto
processor = TextProcessor()

# Otimizar o texto
optimized_text = processor.optimize_for_speech(input_text)

# Salvar textos
original_path = os.path.join(text_dir, f"{base_filename}_original.txt")
optimized_path = os.path.join(text_dir, f"{base_filename}_optimized.txt")

with open(original_path, 'w', encoding='utf-8') as f:
    f.write(input_text)

with open(optimized_path, 'w', encoding='utf-8') as f:
    f.write(optimized_text)

# Exibir resultados
print("\n=== Texto Original ===")
print(input_text)

print("\n=== Texto Otimizado para Fluidez ===")
print(optimized_text)

# Configurações de voz otimizadas para fluidez
voice_settings = {
    "stability": 0.15,          # Ligeiramente aumentado para melhor fluidez (era 0.05)
    "similarity_boost": 0.65,   # Reduzido para fala mais natural e melhor fluidez (era 0.80)
    "style": 0.85,              # Ligeiramente reduzido para melhorar a fluidez (era 1.0)
    "use_speaker_boost": True,  # Melhorar a qualidade do áudio
    "model_id": "eleven_multilingual_v2"  # Modelo multilíngue avançado para melhor sotaque
}

print("\n=== Configurações de Voz Otimizadas para Fluidez ===")
print(json.dumps(voice_settings, indent=2))

print(f"\nResultados salvos em:")
print(f"- Texto original: {original_path}")
print(f"- Texto otimizado: {optimized_path}")
print("\nNenhum crédito foi consumido nesta simulação.")

# Explicação das melhorias
print("\n=== Explicação das Melhorias de Fluidez ===")
print("1. Tratamento seletivo de pontuação:")
print("   - Mantém algumas pontuações para ritmo natural")
print("   - Remove apenas as que causam pausas estranhas")
print("   - Preserva aspas e outros elementos importantes")
print("\n2. Adição de hífens em pontos de quebra natural:")
print("   - Adiciona hífens após conjunções como 'mas', 'e', 'então'")
print("   - Isso cria pausas sutis que melhoram o ritmo natural")
print("\n3. Ajustes nas configurações de voz:")
print("   - Estabilidade aumentada para 0.15 (era 0.05)")
print("   - Boost de similaridade reduzido para 0.65 (era 0.80)")
print("   - Estilo reduzido para 0.85 (era 1.0)")
print("\nEstas mudanças trabalham juntas para criar uma fala mais fluida e natural,")
print("reduzindo as pausas robóticas e melhorando o ritmo geral da narração.")
