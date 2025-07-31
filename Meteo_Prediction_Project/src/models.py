
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def get_models():
    return {
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier()
    }

def get_specific_models(a):
    if a == 0:
        return KNeighborsClassifier(n_neighbors=5)
    elif a ==1:
        return LogisticRegression()
    elif a == 2:
        return DecisionTreeClassifier()
    else:
        return RandomForestClassifier()