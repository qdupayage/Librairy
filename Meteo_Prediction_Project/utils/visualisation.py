
import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation(df):
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Matrice de corrélation")
    plt.tight_layout()
    plt.show()

def plot_predictions(y_true, y_pred, title="Comparaison des valeurs réelles et prédites"):
    plt.figure(figsize=(12, 5))
    plt.plot(y_true.values, label="Réel", alpha=0.7)
    plt.plot(y_pred, label="Prédit", alpha=0.7)
    plt.title(title)
    plt.xlabel("Échantillons")
    plt.ylabel("Valeur")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()