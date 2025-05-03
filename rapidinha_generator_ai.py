"""
Gerador de conteúdo para o quadro "Rapidinha no Cripto" com suporte a IA.
"""
import os
import random
from datetime import datetime
from crypto_news_collector import CryptoNewsCollector
from ai_explainer import AIExplainer

class RapidinhaCryptoGenerator:
    """
    Classe para gerar conteúdo no estilo "Rapidinha no Cripto".
    """

    def __init__(self):
        """
        Inicializa o gerador de conteúdo.
        """
        # Criar diretório para scripts
        self.scripts_dir = os.path.join(os.getcwd(), "scripts")
        os.makedirs(self.scripts_dir, exist_ok=True)

        # Inicializar o explicador de IA
        self.ai_explainer = AIExplainer()

        # Estilo personalizado para o quadro "Rapidinha no Cripto"
        self.style = {
            "saudacao": [
                "Fala cambada!",
                "E aí, cambada!",
                "Beleza, cambada?",
                "E aí cambada, tá ligado?",
                "Salve, salve, cambada!"
            ],
            "introducao": [
                "Bora lá com mais uma Rapidinha Cripto!",
                "Chegou a hora da nossa Rapidinha Cripto!",
                "Vamos para mais uma Rapidinha Cripto de hoje!",
                "Tô de volta com mais uma Rapidinha Cripto!",
                "Partiu mais uma Rapidinha Cripto!"
            ],
            "transicao": [
                "Vamos às notícias!",
                "O que está rolando no mundo cripto?",
                "Quais são as novidades?",
                "Bora ver o que tá bombando no mundo cripto?",
                "Vamos ver o que tá pegando no mercado?"
            ],
            "conclusao": [
                "E é isso por hoje, cambada!",
                "Por hoje é só, cambada!",
                "Essas foram as notícias de hoje!",
                "E aí, o que vocês acharam?",
                "Tropa, tropa, tropa, por hoje é só!"
            ],
            "despedida": [
                "Até a próxima rapidinha!",
                "Nos vemos na próxima rapidinha!",
                "Fiquem ligados para a próxima rapidinha!",
                "Valeu, e até a próxima!",
                "Deixem seus comentários e até mais!"
            ]
        }

        # Dicionário de explicações para notícias simuladas
        self.explanations = self._get_explanations_dict()

    def _get_explanations_dict(self):
        """
        Retorna o dicionário de explicações para notícias simuladas.

        Returns:
            dict: Dicionário com título da notícia como chave e explicação como valor.
        """
        return {
            "Bitcoin atinge novo recorde histórico ultrapassando US$ 100.000":
                "O Bitcoin finalmente quebrou a barreira dos 100 mil dólares! "
                "Isso é como se o seu cafezinho que custava 5 reais agora valesse 50! "
                "Uma valorização incrível que mostra a força dessa criptomoeda como reserva de valor.",

            "Ethereum 2.0 completa transição para Proof of Stake com sucesso":
                "O Ethereum finalmente completou sua transição para o sistema Proof of Stake! "
                "É como se um carro que gastava 20 litros por km agora gastasse apenas 1! "
                "Isso significa transações mais rápidas, taxas menores e muito menos impacto ambiental.",

            "Brasil regulamenta uso de criptomoedas para pagamentos no varejo":
                "Agora é oficial! O Brasil regulamentou o uso de criptomoedas para pagamentos no varejo. "
                "Isso significa que você vai poder comprar seu pãozinho na padaria usando Bitcoin! "
                "A medida deve impulsionar a adoção de criptomoedas no país.",

            "Binance lança nova plataforma de NFTs focada em artistas brasileiros":
                "A Binance acaba de lançar uma plataforma de NFTs exclusiva para artistas brasileiros! "
                "É como um Spotify, mas para arte digital, onde nossos artistas podem monetizar suas criações. "
                "Isso vai abrir portas para muitos talentos nacionais.",

            "Cardano implementa smart contracts para DeFi com foco em sustentabilidade":
                "O Cardano finalmente implementou smart contracts focados em DeFi sustentável! "
                "Imagina poder fazer empréstimos e transações financeiras sem intermediários "
                "e ainda ajudar o meio ambiente."
        }

    def get_mock_news(self):
        """
        Gera notícias fictícias para demonstração.

        Returns:
            list: Lista de notícias fictícias.
        """
        mock_news = [
            {
                "title": "Bitcoin atinge novo recorde histórico ultrapassando US$ 100.000",
                "url": "https://exemplo.com/bitcoin-recorde",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "O Bitcoin finalmente quebrou a barreira dos 100 mil dólares, marcando um momento histórico para a criptomoeda."
            },
            {
                "title": "Ethereum 2.0 completa transição para Proof of Stake com sucesso",
                "url": "https://exemplo.com/ethereum-pos",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A rede Ethereum finalizou sua transição para o mecanismo de consenso Proof of Stake."
            },
            {
                "title": "Brasil regulamenta uso de criptomoedas para pagamentos no varejo",
                "url": "https://exemplo.com/brasil-cripto-regulacao",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "O Banco Central aprovou o uso de criptomoedas como pagamento em estabelecimentos comerciais."
            },
            {
                "title": "Binance lança nova plataforma de NFTs focada em artistas brasileiros",
                "url": "https://exemplo.com/binance-nft-brasil",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A Binance lançou uma plataforma dedicada a NFTs de artistas brasileiros."
            },
            {
                "title": "Cardano implementa smart contracts para DeFi com foco em sustentabilidade",
                "url": "https://exemplo.com/cardano-defi",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A blockchain Cardano lançou sua plataforma de contratos inteligentes com foco em sustentabilidade."
            }
        ]
        return mock_news

    def select_top_news(self, news, count=3):
        """
        Seleciona as notícias mais relevantes.

        Args:
            news (list): Lista de notícias.
            count (int): Número de notícias a selecionar.

        Returns:
            list: Lista das notícias mais relevantes.
        """
        # Simplesmente pegamos as primeiras 'count' notícias
        return news[:count]

    def generate_explanation(self, news_item, use_ai=True):
        """
        Gera uma explicação para uma notícia no estilo "Rapidinha no Cripto".

        Args:
            news_item (dict): Item de notícia.
            use_ai (bool): Se True, tenta usar IA para gerar a explicação.

        Returns:
            str: Explicação gerada.
        """
        title = news_item["title"]

        # Verificar se temos uma explicação pré-definida para esta notícia
        if title in self.explanations:
            return self.explanations[title]

        # Se não tiver explicação pré-definida e use_ai for True, usar IA
        if use_ai:
            return self.ai_explainer.get_explanation(news_item)

        # Se não tiver explicação pré-definida e use_ai for False, gerar uma genérica
        return (
            f"A notícia '{title}' mostra mais um avanço importante no mundo das criptomoedas. "
            "Isso pode impactar diretamente como investimos e usamos moedas digitais no dia a dia."
        )

    def generate_script(self, top_news, use_ai=True):
        """
        Gera um script para o quadro "Rapidinha no Cripto".

        Args:
            top_news (list): Lista das notícias mais relevantes.
            use_ai (bool): Se True, tenta usar IA para gerar explicações.

        Returns:
            str: Script gerado.
        """
        # Saudação
        script = random.choice(self.style["saudacao"]) + " "
        script += random.choice(self.style["introducao"]) + "\n\n"

        # Transição para as notícias
        script += random.choice(self.style["transicao"]) + "\n\n"

        # Explicação de cada notícia
        for i, news in enumerate(top_news, 1):
            script += f"{i}. {news['title']}\n"
            script += self.generate_explanation(news, use_ai=use_ai) + "\n\n"

        # Conclusão e despedida
        script += random.choice(self.style["conclusao"]) + " "
        script += random.choice(self.style["despedida"]) + "\n"

        return script

    def save_script(self, script):
        """
        Salva o script gerado em um arquivo.

        Args:
            script (str): Script gerado.

        Returns:
            str: Caminho do arquivo salvo.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.scripts_dir, f"rapidinha_script_{timestamp}.txt")

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(script)

        print(f"Script salvo em {filename}")
        return filename

    def get_real_news(self):
        """
        Obtém notícias reais usando o coletor de notícias.

        Returns:
            list: Lista de notícias reais.
        """
        try:
            # Usar o coletor de notícias para obter notícias reais
            collector = CryptoNewsCollector()
            news = collector.collect_all_news()

            if news:
                print(f"Coletadas {len(news)} notícias reais.")
                return news

            print("Não foi possível coletar notícias reais. Usando notícias simuladas.")
            return self.get_mock_news()

        except Exception as e:
            print(f"Erro ao coletar notícias reais: {e}. Usando notícias simuladas.")
            return self.get_mock_news()

    def create_rapidinha(self, use_real_news=True, use_ai=True):
        """
        Processo completo para criar um novo episódio de "Rapidinha no Cripto".

        Args:
            use_real_news (bool): Se True, tenta usar notícias reais. Se False, usa notícias simuladas.
            use_ai (bool): Se True, tenta usar IA para gerar explicações.

        Returns:
            str: Caminho do script gerado.
        """
        # Obter notícias (reais ou simuladas)
        news = self.get_real_news() if use_real_news else self.get_mock_news()

        # Selecionar as mais relevantes
        top_news = self.select_top_news(news)

        # Gerar o script
        script = self.generate_script(top_news, use_ai=use_ai)

        # Salvar o script
        return self.save_script(script)


if __name__ == "__main__":
    import argparse

    # Configurar argumentos de linha de comando
    parser = argparse.ArgumentParser(
        description="Gerador de conteúdo para o quadro 'Rapidinha no Cripto'"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Usar notícias simuladas em vez de notícias reais"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Não usar IA para gerar explicações"
    )
    args = parser.parse_args()

    # Criar o gerador e gerar o script
    generator = RapidinhaCryptoGenerator()
    script_path = generator.create_rapidinha(
        use_real_news=not args.mock,
        use_ai=not args.no_ai
    )

    print("Novo episódio de 'Rapidinha no Cripto' criado com sucesso!")

    # Exibir o script
    with open(script_path, 'r', encoding='utf-8') as file:
        print("\n" + "="*50 + "\n")
        print(file.read())
        print("\n" + "="*50 + "\n")
