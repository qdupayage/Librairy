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

def estimate_electricity_price(df, production_columns, cost_dict, demand_column):
    """
    Estime le prix moyen de l'électricité à partir des coûts de production et de la demande.

    Parameters:
        df (pd.DataFrame): contient les colonnes de production et de demande
        production_columns (list): noms des colonnes correspondant aux productions par source
        cost_dict (dict): coût unitaire de chaque source, e.g. {'nuclear': 20, 'wind': 10}
        demand_column (str): nom de la colonne de demande

    Returns:
        pd.Series: série temporelle du prix de l'électricité estimé
    """
    total_cost = pd.Series(0.0, index=df.index)
    total_production = pd.Series(0.0, index=df.index)

    for col in production_columns:
        if col in df.columns and col in cost_dict:
            total_cost += df[col] * cost_dict[col]
            total_production += df[col]

    # éviter division par zéro
    unit_price = total_cost / total_production.replace(0, np.nan)

    # Ajuster si la demande est plus grande que la production
    if demand_column in df.columns:
        supply_ratio = df[demand_column] / total_production.replace(0, np.nan)
        unit_price *= supply_ratio.clip(lower=1.0)  # surcharge si demande > production

    return unit_price.fillna(0)