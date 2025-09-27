# Atividade de coleta e mineração de dados requerida como parte da média trimestral da disciplina Datamining e Webscraping (F105) do curso de ADS da UNIFOR.

## Equipe
- Isaias do Amaral Sousa - 2416767
- Elias Batista Souza - 2415532
- Lais Dantas Ferreira - 2418863
- Isadora Furtado Menezes - 
- Francisca Fernanda Lemos de Oliveira - 2424120
- Rafael Angelo Pinheiro do Vale - 2418273

# Objetivo:
Coletar comentários das últimas 30 postagens de um perfil do X, pré-processar, classificar sentimentos com a biblioteca LeIA do Python e gerar gráficos.

# Descrição
O aluno deverá desenvolver um sistema capaz de capturar os comentários das últimas 30 postagens (de forma automatizada) realizadas por um portal de notícias na rede social X (ex-Twitter). Essa captura deve utilizar a biblioteca Selenium do Python Os dados coletados devem ser armazenados em um arquivo CSV no formato sugerido na
Figura 1 (imagem no PDF no sistema EAD).

Com a base de dados em mãos, o aluno deverá identificar automaticamente o sentimento expresso em cada comentário utilizando a biblioteca LeIA para Python. O arquivo CSV deverá ser atualizado com uma nova coluna chamada sentimento, que deverá conter apenas um dos seguintes valores:
- POSITIVO
- NEGATIVO
- NEUTRO
Essa coluna indicará qual sentimento o comentário expressa em relação ao post analisado.

Por fim, o aluno deverá realizar uma análise dos dados obtidos, apresentando um gráfico de barras que mostre a quantidade de comentários positivos, negativos e neutros para cada notícia coletada.

## Como executar o projeto:
1. Criar e ativar ambiente virtual.
    - python -m venv .venv (cria o ambiente virtual).
    - .\.venv\Scripts\Activate.ps1 (ativa o ambiente virtual).
2. Executar no terminal 'pip install -r requirements.txt' para instalar as extensões.
3. Ajustar seletores em 'scraper.py' (caso alguma marcação HTML seja alterada pelo X).
4. Executar no terminal 'python main.py --profile "@g1" --limit 30' (coleta as últimas 30 postagens do portal de notícias G1).

## Saída
- 'outputs/dataset.csv' com colunas: 'codigo_da_postagem, conta, texto_da_postagem, sentimento'
