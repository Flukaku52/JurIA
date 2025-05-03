"""
Módulo para coletar notícias reais sobre criptomoedas de diversas APIs.
"""
import os
import json
import requests
from datetime import datetime
import time
import random
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class CryptoNewsCollector:
    """
    Classe para coletar notícias reais sobre criptomoedas de diversas APIs.
    """
    
    def __init__(self):
        """
        Inicializa o coletor de notícias.
        """
        # Diretório para salvar as notícias coletadas
        self.data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Chaves de API (obtidas de variáveis de ambiente ou valores padrão para testes)
        self.cryptocompare_api_key = os.getenv("CRYPTOCOMPARE_API_KEY", "")
        self.newsapi_key = os.getenv("NEWSAPI_KEY", "")
        
        # Headers para requisições HTTP
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_cryptocompare_news(self):
        """
        Coleta notícias da API CryptoCompare.
        
        Returns:
            list: Lista de notícias coletadas.
        """
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=PT"
        
        # Adicionar categorias e chave de API se disponível
        if self.cryptocompare_api_key:
            url += f"&api_key={self.cryptocompare_api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            news = []
            if 'Data' in data:
                for article in data['Data'][:10]:  # Limitar a 10 notícias
                    news.append({
                        "title": article.get('title', ''),
                        "url": article.get('url', ''),
                        "source": article.get('source', 'CryptoCompare'),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "content": article.get('body', '')
                    })
            
            print(f"Coletadas {len(news)} notícias da CryptoCompare API")
            return news
        except Exception as e:
            print(f"Erro ao coletar notícias da CryptoCompare API: {e}")
            return []
    
    def get_newsapi_crypto_news(self):
        """
        Coleta notícias sobre criptomoedas da NewsAPI.
        
        Returns:
            list: Lista de notícias coletadas.
        """
        if not self.newsapi_key:
            print("Chave da NewsAPI não configurada. Pulando esta fonte.")
            return []
        
        url = f"https://newsapi.org/v2/everything?q=bitcoin OR cryptocurrency OR blockchain&language=pt&sortBy=publishedAt&apiKey={self.newsapi_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            news = []
            if 'articles' in data:
                for article in data['articles'][:10]:  # Limitar a 10 notícias
                    news.append({
                        "title": article.get('title', ''),
                        "url": article.get('url', ''),
                        "source": article.get('source', {}).get('name', 'NewsAPI'),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "content": article.get('description', '')
                    })
            
            print(f"Coletadas {len(news)} notícias da NewsAPI")
            return news
        except Exception as e:
            print(f"Erro ao coletar notícias da NewsAPI: {e}")
            return []
    
    def get_coingecko_market_data(self):
        """
        Coleta dados de mercado da API CoinGecko e transforma em notícias.
        
        Returns:
            list: Lista de notícias geradas a partir dos dados de mercado.
        """
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            news = []
            for coin in data:
                # Criar uma "notícia" baseada nos dados de mercado
                price_change = coin.get('price_change_percentage_24h', 0)
                direction = "sobe" if price_change > 0 else "cai"
                
                title = f"{coin.get('name', '')} {direction} {abs(price_change):.2f}% nas últimas 24 horas"
                content = (
                    f"O preço do {coin.get('name', '')} ({coin.get('symbol', '').upper()}) "
                    f"está em US$ {coin.get('current_price', 0):,.2f}, com uma variação de "
                    f"{price_change:.2f}% nas últimas 24 horas. "
                    f"Volume de negociação: US$ {coin.get('total_volume', 0):,.2f}. "
                    f"Capitalização de mercado: US$ {coin.get('market_cap', 0):,.2f}."
                )
                
                news.append({
                    "title": title,
                    "url": f"https://www.coingecko.com/pt/moedas/{coin.get('id', '')}",
                    "source": "CoinGecko",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "content": content
                })
            
            print(f"Coletadas {len(news)} notícias de mercado da CoinGecko API")
            return news
        except Exception as e:
            print(f"Erro ao coletar dados de mercado da CoinGecko API: {e}")
            return []
    
    def get_mock_news(self):
        """
        Gera notícias fictícias para testes quando as APIs reais falham.
        
        Returns:
            list: Lista de notícias fictícias.
        """
        mock_news = [
            {
                "title": "Bitcoin atinge novo recorde histórico ultrapassando US$ 100.000",
                "url": "https://exemplo.com/bitcoin-recorde",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "O Bitcoin finalmente quebrou a barreira dos 100 mil dólares, marcando um momento histórico para a criptomoeda. Especialistas atribuem a alta à crescente adoção institucional e à escassez programada da moeda."
            },
            {
                "title": "Ethereum 2.0 completa transição para Proof of Stake com sucesso",
                "url": "https://exemplo.com/ethereum-pos",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A rede Ethereum finalizou com sucesso sua transição para o mecanismo de consenso Proof of Stake, reduzindo drasticamente o consumo de energia e aumentando a escalabilidade da rede."
            },
            {
                "title": "Brasil regulamenta uso de criptomoedas para pagamentos no varejo",
                "url": "https://exemplo.com/brasil-cripto-regulacao",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "O Banco Central do Brasil aprovou regulamentação que permite o uso de criptomoedas como meio de pagamento em estabelecimentos comerciais, colocando o país na vanguarda da adoção de moedas digitais."
            },
            {
                "title": "Binance lança nova plataforma de NFTs focada em artistas brasileiros",
                "url": "https://exemplo.com/binance-nft-brasil",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A Binance, maior exchange de criptomoedas do mundo, lançou uma plataforma dedicada a NFTs de artistas brasileiros, com foco em promover a cultura nacional através da tecnologia blockchain."
            },
            {
                "title": "Cardano implementa smart contracts para DeFi com foco em sustentabilidade",
                "url": "https://exemplo.com/cardano-defi",
                "source": "Notícias Simuladas",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": "A blockchain Cardano lançou sua plataforma de contratos inteligentes com foco em aplicações DeFi sustentáveis, prometendo transações mais eficientes energeticamente que suas concorrentes."
            }
        ]
        return mock_news
    
    def filter_relevant_news(self, news_list, keywords=None):
        """
        Filtra notícias relevantes com base em palavras-chave.
        
        Args:
            news_list (list): Lista de notícias para filtrar.
            keywords (list): Lista de palavras-chave para filtrar. Se None, usa palavras-chave padrão.
            
        Returns:
            list: Lista de notícias filtradas.
        """
        if not keywords:
            keywords = [
                "bitcoin", "ethereum", "cripto", "blockchain", "defi", 
                "nft", "regulação", "cbdc", "altcoin", "mercado"
            ]
        
        filtered_news = []
        
        for news in news_list:
            title = news.get("title", "").lower()
            content = news.get("content", "").lower()
            
            # Verificar se alguma palavra-chave está presente no título ou conteúdo
            if any(keyword in title or keyword in content for keyword in keywords):
                filtered_news.append(news)
        
        return filtered_news
    
    def collect_all_news(self):
        """
        Coleta notícias de todas as fontes configuradas.
        
        Returns:
            list: Lista combinada de notícias de todas as fontes.
        """
        all_news = []
        
        # CryptoCompare API
        news = self.get_cryptocompare_news()
        all_news.extend(news)
        
        # NewsAPI
        news = self.get_newsapi_crypto_news()
        all_news.extend(news)
        
        # CoinGecko Market Data
        news = self.get_coingecko_market_data()
        all_news.extend(news)
        
        # Se não conseguiu coletar notícias de nenhuma fonte, usa as notícias fictícias
        if not all_news:
            print("Não foi possível coletar notícias reais. Usando notícias simuladas para testes...")
            all_news = self.get_mock_news()
        
        # Filtrar notícias relevantes
        filtered_news = self.filter_relevant_news(all_news)
        
        # Remover duplicatas (baseado no título)
        unique_news = []
        titles = set()
        
        for news in filtered_news:
            title = news.get("title")
            if title and title not in titles:
                titles.add(title)
                unique_news.append(news)
        
        # Salvar as notícias coletadas
        self.save_news(unique_news)
        
        return unique_news
    
    def save_news(self, news):
        """
        Salva as notícias coletadas em um arquivo JSON.
        
        Args:
            news (list): Lista de notícias para salvar.
        """
        filename = os.path.join(self.data_dir, f"crypto_news_{datetime.now().strftime('%Y%m%d')}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news, f, ensure_ascii=False, indent=4)
        
        print(f"Notícias salvas em {filename}")


if __name__ == "__main__":
    collector = CryptoNewsCollector()
    news = collector.collect_all_news()
    print(f"Coletadas {len(news)} notícias sobre criptomoedas no total.")
