import seaborn as sns
import matplotlib.pyplot as plt

def plot_clusters(df):
    sns.pairplot(df, hue="cluster", vars=["age", "education-num", "hours-per-week"])
    plt.suptitle("Clusters sociaux", y=1.02)
    plt.show()
