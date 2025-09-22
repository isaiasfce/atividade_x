import pandas as pd
import matplotlib.pyplot as plt

def plot_by_post(csv_path="outputs/dataset.csv", out_image="outputs/sentiment_by_post.png"):
    df = pd.read_csv(csv_path)
    counts = df.groupby(["codigo_da_postagem","sentimento"]).size().unstack(fill_value=0)
    ax = counts.plot(kind='bar', figsize=(14,6))
    ax.set_xlabel("Código da Postagem")
    ax.set_ylabel("Número de comentários")
    ax.set_title("Distribuição de Sentimentos por Notícia")
    plt.legend(title="Sentimento")
    plt.tight_layout()
    plt.savefig(out_image)
    print(f"Gráfico salvo em {out_image}")
