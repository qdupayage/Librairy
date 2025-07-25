
import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation(df):
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Matrice de corrélation")
    plt.tight_layout()
    plt.show()
