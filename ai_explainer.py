"""
Módulo para gerar explicações para notícias usando a API da OpenAI.
"""
import os
import json
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class AIExplainer:
    """
    Classe para gerar explicações para notícias usando a API da OpenAI.
    """

    def __init__(self):
        """
        Inicializa o explicador de IA.
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Aviso: API key da OpenAI não encontrada. Usando explicações genéricas.")

        # Diretório para cache de explicações
        self.cache_dir = os.path.join(os.getcwd(), "cache")
        os.makedirs(self.cache_dir, exist_ok=True)

        # Carregar cache existente
        self.cache = self._load_cache()

        # Estilo para as explicações
        self.style_prompt = """
"E aí cambada, tô de volta com o resumo dax últimax notíciax de cripto, bora lá? Com meu sotaque carioca bem característico, vamox falar sobre a mais recente 'baleia do mercado', que decidiu nadar nax águax do Bitcoin. Sabe o que isso significa, né? Isso mesmo, tá rolando um 'índice de acumulação' altíssimo. Pra quem não tá ligado no que é isso, é como se o 'papai noel' tivesse descido a chaminé mais cedo e deixado um presentão debaixo da árvore.

Mas ó, não se iluda, hein? Investir em Bitcoin não é como acreditar em 'papai noel'. Tem que se ligar nox riscox, e não sair acreditando em promessa de retorno milagroso. Pra mim, tem aquele cheirinho de cilada quando a promessa é grande demais, sabe?

Agora, mudando de assunto, teve um 'evento cripto' recentemente que chamou a atenção. Foi o 'Digital Asset Summer', e teve gente grande do setor falando sobre o futuro dax criptox, inclusive do Bitcoin. E aí, será que o Bitcoin vai ser o 'porto seguro' do futuro, ou vai ser mais uma 'tesouraria da empresa'?

Por fim, quer sentar, quer sentar, quer, quer sentar? Pois é, tem gente que tá vendo Bitcoin como esquema de pirâmide. Mas ó, deixa eu te contar uma coisa: Bitcoin não é pirâmide financeira. Na verdade, pirâmide financeira é aquele esquema em que você tem que trazer mais gente pra ganhar dinheiro, sabe? Tipo um 'esquema ponzi'. Bitcoin não é isso não, vamox deixar isso bem claro, tropa, tropa, tropa, tropa, tropa.

E aí, o que vocês acham? Vale a pena investir no Bitcoin, ou é melhor ficar de olho em outrax criptox? Deixem suax opiniõex nox comentáriox. Valeu, e até a próxima!"

Características do meu estilo de fala:
1. Sotaque carioca bem característico, especialmente o chiado nos 's' finais das palavras (que soam como 'x')
2. Uso frequente da palavra "cambada" (NUNCA uso "galera")
3. Uso frequente de expressões como "bora lá", "tá ligado", "tropa" (NÃO uso muitas gírias cariocas típicas)
4. Expressões de entusiasmo como "Isso mesmo!", "Olha só!", "Inacreditável!"
5. Uso de analogias simples para explicar conceitos complexos
6. Tom conversacional e informal, como se estivesse falando com amigos
7. Frases curtas e diretas, evitando linguagem técnica demais
8. Perguntas retóricas para engajar o público
9. Referências a memes e cultura pop
10. Uso de expressões como "quer sentar, quer sentar" e repetição de palavras como "tropa, tropa, tropa"
11. Explicações simplificadas para iniciantes no mundo cripto
12. Sempre alerto sobre riscos, mas mantendo um tom otimista
13. O nome do quadro é "Rapidinha Cripto" (sem o "no")
"""

    def _load_cache(self):
        """
        Carrega o cache de explicações do disco.

        Returns:
            dict: Cache de explicações.
        """
        cache_file = os.path.join(self.cache_dir, "explanations_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar cache: {e}")
        return {}

    def _save_cache(self):
        """
        Salva o cache de explicações no disco.
        """
        cache_file = os.path.join(self.cache_dir, "explanations_cache.json")
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")

    def get_explanation(self, news_item):
        """
        Gera uma explicação para uma notícia usando a API da OpenAI.

        Args:
            news_item (dict): Item de notícia.

        Returns:
            str: Explicação gerada.
        """
        title = news_item.get("title", "")
        content = news_item.get("content", "")

        # Verificar se já temos uma explicação em cache
        cache_key = title
        if cache_key in self.cache:
            print(f"Usando explicação em cache para: {title}")
            return self.cache[cache_key]

        # Se não temos API key ou conteúdo, retornar explicação genérica
        if not self.api_key or not content:
            explanation = self._generate_generic_explanation(title)
            self.cache[cache_key] = explanation
            self._save_cache()
            return explanation

        # Gerar explicação usando a API da OpenAI
        try:
            explanation = self._call_openai_api(title, content)

            # Salvar no cache
            self.cache[cache_key] = explanation
            self._save_cache()

            return explanation
        except Exception as e:
            print(f"Erro ao gerar explicação com IA: {e}")
            explanation = self._generate_generic_explanation(title)
            return explanation

    def _call_openai_api(self, title, content):
        """
        Chama a API da OpenAI para gerar uma explicação.

        Args:
            title (str): Título da notícia.
            content (str): Conteúdo da notícia.

        Returns:
            str: Explicação gerada.
        """
        url = "https://api.openai.com/v1/chat/completions"

        # Preparar o prompt
        prompt = f"{self.style_prompt}\n\nTítulo: {title}\n\nConteúdo: {content}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Você é um assistente especializado em criar conteúdo sobre criptomoedas no estilo de Renato Santanna Silva, com seu característico sotaque carioca. Enfatize o chiado nos 's' finais das palavras (que soam como 'x'). Use 'cambada' em vez de 'galera', expressões de entusiasmo, analogias simples, tom conversacional, frases curtas e diretas, perguntas retóricas, referências a memes, e repetições características como 'tropa, tropa, tropa'."},
                {"role": "user", "content": prompt + "\n\nIMPORTANTE: Limite sua resposta a no máximo 3-4 frases curtas. Seja direto, objetivo e use meu estilo característico com gírias e expressões."}
            ],
            "max_tokens": 150,
            "temperature": 0.8
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        explanation = result["choices"][0]["message"]["content"].strip()

        # Adicionar um pequeno atraso para evitar atingir limites de taxa
        time.sleep(1)

        return explanation

    def _generate_generic_explanation(self, title):
        """
        Gera uma explicação genérica para uma notícia.

        Args:
            title (str): Título da notícia.

        Returns:
            str: Explicação genérica.
        """
        return (
            f"A notícia '{title}' mostra mais um avanço importante no mundo das criptomoedas. "
            "Isso pode impactar diretamente como investimos e usamos moedas digitais no dia a dia."
        )


if __name__ == "__main__":
    # Teste simples
    explainer = AIExplainer()

    test_news = {
        "title": "Bitcoin ultrapassa US$ 50.000 pela primeira vez em 2023",
        "content": "O Bitcoin superou a marca de US$ 50.000 nesta segunda-feira, atingindo seu maior valor desde dezembro de 2021. Analistas atribuem a alta à crescente adoção institucional e à expectativa de aprovação de ETFs de Bitcoin à vista nos Estados Unidos."
    }

    explanation = explainer.get_explanation(test_news)
    print(f"\nNotícia: {test_news['title']}")
    print(f"Explicação: {explanation}")
