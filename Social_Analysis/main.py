from src.load_data import load_adult_dataset
from src.analysis import group_by_income
from src.clustering import cluster_individuals
from src.viz import plot_clusters

df = load_adult_dataset()
print(group_by_income(df))
df_clustered, _ = cluster_individuals(df)
plot_clusters(df_clustered)
