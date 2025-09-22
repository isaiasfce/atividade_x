import argparse #permite que executemos o comando --profile @nomedeusuario
from scraper import start_driver, collect_last_posts_with_comments #inicia o navegador e a coleta de dados
from preprocess import clean_text #limpa o texto dos comentários
from sentiment import classify_sentiment #faz a análise de sentimento
import pandas as pd #chama a biblioteca pandas

#define a função principal para execução do scraper
def main(profile: str, limit: int, headless: bool = True): #nome do perfil / num. de posts coletados / para que o navegador seja rodado em segundo plano
    driver = start_driver(headless=headless) #inicializa o navegador
    try: #inicia a coleta e classificação
        #1. coleta de dados
        #usa o scraper para coletar as postagens e seus comentários
        posts = collect_last_posts_with_comments(driver, profile, limit)
        
        #cria uma lista vazia para armazenar os dados coletados
        rows = []

        #2. processar cada um dos dados pegues
        #loop para percorrer cada postagem encontrada
        for post in posts:
            #loop para percorrer cada comentário dentro da postagem atual
            for comment in post["comentarios"]:

                #limpa o texto do comentário
                cleaned = clean_text(comment)

                #analisa o sentimento do texto já limpo
                sentimento = classify_sentiment(cleaned)

                #adiciona uma nova "linha" de dados a nossa lista de resultados
                rows.append({
                    "codigo_da_postagem": post["codigo"],
                    "conta" : profile,
                    "texto_da_postagem": post["texto_post"],
                    "texto_do_comentario": cleaned,
                    "sentimento": sentimento
                })
        #3. salvar o resultado
        #transforma a lista de dados em uma tabela do Pandas
        df = pd.DataFrame(rows, columns=["codigo_da_postagem","conta","texto_da_postagem","texto_do_comentario","sentimento"])

        #salva a tabela em um arquivo csv na pasta "outputs"
        df.to_csv("outputs/dataset.csv", index=False)

        #mensagem de confirmação
        print("Dataset salvo em outputs/dataset.csv")

    finally:
        #fecha o navegador ao final da execução
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="@tvm")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--headless", type=bool, default=True)
    args = parser.parse_args()
    main(args.profile, args.limit, args.headless)