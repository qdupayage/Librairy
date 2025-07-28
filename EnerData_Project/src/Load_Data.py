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

def construct_dataframe(df, countries, production_name=[], Interconnexions=True, Demand=True, Price=True):
    """s
    Construit un DataFrame horodaté avec les données sélectionnées pour les pays donnés.

    Args:
        df (pd.DataFrame): DataFrame d'origine contenant les données horodatées.
        countries (list): Liste des pays à inclure.
        production_name (list): Liste des types de productions à inclure (ex: ["Wind", "Solar"]).
        Interconnexions (bool): Inclure les interconnexions si True.
        Demand (bool): Inclure la demande si True.
        Price (bool): Inclure le prix si True.

    Returns:
        pd.DataFrame: DataFrame construit avec les colonnes demandées.
    """

    # Vérifier que 'DateTime' est bien indexé ou présent
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)

    result_df = pd.DataFrame(index=df.index)

    for country in countries:
        # Production
        for prod in production_name:
            col_name = f"Prod_{prod}_{country}"
            if col_name in df.columns:
                result_df[col_name] = df[col_name]

        # Interconnexions
        if Interconnexions:
            # On suppose que les colonnes sont sous forme 'link_country1_country2'
            interco_cols = [col for col in df.columns if col.startswith('link_') and f"_{country}" in col]
            for col in interco_cols:
                result_df[col] = df[col]

        # Demande
        if Demand:
            demand_col = f"Demand_{country}"
            if demand_col in df.columns:
                result_df[demand_col] = df[demand_col]

        # Prix
        if Price:
            price_col = f"Price_{country}"
            if price_col in df.columns:
                result_df[price_col] = df[price_col]

    return result_df