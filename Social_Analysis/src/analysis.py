def summarize_data(df):
    return df.describe(include="all")

def group_by_income(df):
    return df.groupby("income")[["age", "education-num", "hours-per-week"]].mean()
