import pandas as pd
import numpy as np
from pathlib import Path

def load_excel(filepath: str, sheet_name=0) -> pd.DataFrame:
    """Charge un fichier Excel horodaté."""
    df = pd.read_excel(filepath, sheet_name=sheet_name, parse_dates=['DateTime'])
    return df

def load_parquet(filepath: str) -> pd.DataFrame:
    """Charge un fichier parquet horodaté."""
    df = pd.read_parquet(filepath)
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df

def construct_dataframe(df, countries, time_range=['2023-01-01', '2023-01-03'],
                        production_name=[], Interconnexions=True, Demand=True, Price=True,
                        freq='h'):
    """
    Construit un DataFrame horodaté avec les données sélectionnées pour les pays donnés.

    Args:
        df (pd.DataFrame): DataFrame d'origine contenant les données horodatées.
        countries (list): Liste des pays à inclure.
        time_range (list): Liste des dates de début et de fin de période
        production_name (list): Liste des types de productions à inclure (ex: ["Wind", "Solar"]).
        Interconnexions (bool): Inclure les interconnexions si True.
        Demand (bool): Inclure la demande si True.
        Price (bool): Inclure le prix si True.
        freq (str): Fréquence des données (par défaut 'H' pour horaire)

    Returns:
        pd.DataFrame: DataFrame construit avec les colonnes demandées.
    """

    # Base temporelle (index commun)
    datetime_index = pd.date_range(start=time_range[0], end=time_range[1], freq=freq)
    result_df = pd.DataFrame(index=datetime_index)
    result_df.index.name = 'DateTime'

    # Assurer que la colonne DateTime est bien en datetime
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df.set_index('DateTime')

    for country in countries:
        # Production : on ajoute chaque prod demandée
        for prod in production_name:
            col_name = f"Prod_{prod}_{country}"
            if col_name in df.columns:
                result_df = result_df.join(df[[col_name]], how='left')

        # Interconnexions
        if Interconnexions:
            interco_cols = [col for col in df.columns if col.startswith('link_') and f"_{country}" in col]
            result_df = result_df.join(df[interco_cols], how='left')

        # Demande
        if Demand:
            demand_col = f"Demand_{country}"
            if demand_col in df.columns:
                result_df = result_df.join(df[[demand_col]], how='left')

        # Prix
        if Price:
            price_col = f"Price_{country}"
            if price_col in df.columns:
                result_df = result_df.join(df[[price_col]], how='left')

    return result_df.reset_index()

def read_csv(path):
    """
    Corrige les erreurs dues à un CSV avec une ligne DateTime mal alignée.
    Reconstruit correctement le DataFrame avec les colonnes et les données alignées.
    """
    # Lire tout le fichier sans traiter les en-têtes
    raw_df = pd.read_csv(path, header=None)

    # Ligne 0 contient les noms de colonnes
    column_names = raw_df.iloc[0].tolist()
    
    # Ligne 2+ contient les vraies données
    data = raw_df.iloc[2:].reset_index(drop=True)
    data.columns = column_names

    # Créer un DateTime bien formatté
    if 'DateTime' in data.columns:
        data['DateTime'] = pd.to_datetime(data['DateTime'])
    else:
        # Cas rare : DateTime est uniquement dans la 2e ligne
        datetime_values = pd.to_datetime(raw_df.iloc[1, 1:].dropna().tolist())
        data['DateTime'] = datetime_values

    return data
