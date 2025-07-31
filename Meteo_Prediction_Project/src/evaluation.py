
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(f"🔢 MAE : {mae:.4f}")
    print(f"📉 MSE : {mse:.4f}")
    print(f"📈 RMSE : {rmse:.4f}")
    print(f"📊 R² : {r2:.4f}")

    return {
        "model": model,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }