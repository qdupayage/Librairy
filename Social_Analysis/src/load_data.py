import pandas as pd

def load_adult_dataset(path="data/raw/adult.data"):
    cols = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
            "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
            "hours-per-week", "native-country", "income"]
    df = pd.read_csv(path, names=cols, na_values=" ?", skipinitialspace=True)
    return df.dropna()
