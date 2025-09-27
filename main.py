import argparse
import pandas as pd
from scraper import start_driver, login_and_wait, collect_last_posts_with_comments
from preprocess import clean_text
from sentiment import classify_sentiment
from visualize import plot_by_post

def main(profile: str, limit: int, headless: bool = True):
    
    """
    Descrição do fluxo da execução do projeto:
    1. Inicia o navegador
    2. Realiza o login
    3. Coleta posts e comentários
    4. Pré-processa os textos
    5. Analisa o sentimento
    6. Salva o dataset em CSV
    7. Gera o gráfico de visualização
    """
    
    driver = start_driver(headless=headless) 
    try:
        # 0. Login na rede X
        if not login_and_wait(driver, wait_time=120):
            print("Login falhou. Encerrando o script.")
            return

        # 1. Coleta de dados
        print(f"\nIniciando coleta de {limit} posts do perfil {profile}...")
        posts = collect_last_posts_with_comments(driver, profile, limit)
        
        if not posts:
            print("Nenhum post foi retornado pelo scraper. O CSV não será gerado.")
            return

        # 2. Processamento dos dados
        rows = []
        total_comments = sum(len(p.get("comentarios", [])) for p in posts)
        print(f"\nProcessando um total de {total_comments} comentários de {len(posts)} posts...")

        for post in posts:
            for comment in post.get("comentarios", []):
                cleaned = clean_text(comment)
                # Ignora comentários que ficaram vazios após a limpeza
                if not cleaned:
                    continue
                
                sentimento = classify_sentiment(cleaned)
                # Adiciona os comentários a lista
                rows.append({
                    "codigo_da_postagem": post["codigo"],
                    "conta": profile.lstrip('@'),
                    "texto_da_postagem": post["texto_post"],
                    "texto_do_comentario": cleaned,
                    "sentimento": sentimento
                })
        
        if not rows:
            print("\nNenhum comentário válido foi processado. O arquivo CSV estará vazio.")
            return

        # 3. Salvamento do resultado
        print(f"\nProcessamento finalizado. Salvando {len(rows)} comentários no CSV...")
        output_path = "outputs/dataset.csv"
        df = pd.DataFrame(rows, columns=[
            "codigo_da_postagem", "conta", "texto_da_postagem", 
            "texto_do_comentario", "sentimento"
        ])
        df.to_csv(output_path, index=False)
        print(f"Dataset salvo com sucesso em {output_path}!")

        # 4. Geração do gráfico
        print("\nGerando gráfico de análise de sentimento...")
        plot_by_post(csv_path=output_path)

    finally:
        print("\nFechando o navegador.")
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coleta e analisa posts e comentários do X (aka Twitter).")
    parser.add_argument("--profile", default="@g1", help="Perfil do X para coletar os dados.")
    parser.add_argument("--limit", type=int, default=3, help="Número de posts para coletar.") # Reduzido para testes
    parser.add_argument("--headless", type=bool, default=False, help="Executar o navegador em modo invisível.") # Alterado para visível por padrão
    args = parser.parse_args()
    main(args.profile, args.limit, args.headless)