from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def cluster_individuals(df, n_clusters=4):
    features = ["age", "education-num", "hours-per-week"]
    X = df[features]
    X_scaled = StandardScaler().fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df["cluster"] = kmeans.fit_predict(X_scaled)
    return df, kmeans
