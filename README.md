# Atividade de coleta e mineração de dados requerida como parte da média trimestral da disciplina Datamining e Webscraping (F105) do curso de ADS da UNIFOR.

# Objetivo:
Coletar comentários das últimas 30 postagens de um perfil do X, pré-processar, classificar sentmentos com LeIA e gerar gráficos.

## Como executar o projeto:
1. Criar e ativar ambiente virtual.
2. 'pip install -r requirements.txt'
3. Ajustar seletores em 'scraper.py'
4. 'python main.py --profile @tvm --limit 30'

## Saída
- 'outputs/dataset.csv' com colunas: 'codigo_da_postagem, conta, texto_da_postagem, sentimento'
