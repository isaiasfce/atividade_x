# Importe a classe do módulo 'leia'
from LeIA import SentimentIntensityAnalyzer

# 1. Crie UMA instância do analisador. Faça isso apenas uma vez.
analisador = SentimentIntensityAnalyzer()

# Lista de frases que você quer analisar
frases_para_testar = [
    "esse produto é maravilhoso",
    "eu odiei o serviço, foi péssimo",
    "o filme foi ok, nem bom nem ruim"
]

# Itere sobre a lista e analise cada frase
for frase in frases_para_testar:
    # 2. Use o método .polarity_scores() no objeto para obter os scores
    scores = analisador.polarity_scores(frase)
    
    # 3. Imprima o resultado de forma clara
    print(f"Frase: '{frase}' -> Scores: {scores}")