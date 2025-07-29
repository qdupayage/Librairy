import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_timeseries(df, variables, title=None, ylabel=None, legend=True, source_type=''):
    """
    Affiche des courbes temporelles (x = DateTime).
    """
    # Vérifier la présence de DateTime
    if 'DateTime' not in df.columns:
        raise ValueError("Colonne 'DateTime' absente du DataFrame.")

    # Nettoyage : s'assurer que DateTime est bien datetime64
    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

    # Supprimer lignes vides ou incorrectes
    df = df.dropna(subset=['DateTime'])

    # Vérifie si on a des variables valides
    variables_valides = [var for var in variables if var in df.columns]
    if not variables_valides:
        raise ValueError("Aucune variable valide parmi : " + ", ".join(variables))

    # Convertir toutes les autres colonnes en numériques si besoin
    for col in df.columns:
        if col != 'DateTime':
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Affichage
    plt.figure(figsize=(15, 5))

    for var in variables_valides:
        if np.issubdtype(df[var].dtype, np.number):
            # FORCER le x explicite = DateTime
            plt.plot(df['DateTime'], df[var], label=var)
        else:
            print(f"[AVERTISSEMENT] Variable ignorée (non-numérique) : {var}")

    # Ajout titres et légendes
    if title:
        plt.title(f"{title} ({source_type.upper()})" if source_type else title)
    if ylabel:
        plt.ylabel(ylabel)

    plt.xlabel("DateTime")
    if legend:
        plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compute_market_price_by_country(df, cost_dict):
    """
    Calcule le prix spot de l'électricité pour chaque pays selon la logique du merit order,
    en considérant les productions locales et les interconnexions.

    Parameters:
        df (pd.DataFrame): contient les colonnes de production, consommation, interconnexions, etc.
        cost_dict (dict): coûts unitaires des sources (€/MWh)

    Returns:
        pd.DataFrame: prix spot pour chaque pays, colonne par pays
        pd.DataFrame: techno marginale (celle qui fixe le prix) pour chaque heure et chaque pays
    """
    countries = df['country'].unique()

    for country in countries:
        df_country = df[df['country'] == country].copy()
        df_country = df_country.set_index('DateTime')

        # Récupérer toutes les colonnes de production pour ce pays
        prod_cols = [col for col in df_country.columns if col.startswith('prod_') and col.endswith(f"_{country}")]

        # Approximation de la consommation nette = somme production + solde interconnexions
        interco_cols = [col for col in df_country.columns if 'interconnexion' in col.lower() and col.endswith(f"_{country}")]
        solde_interco = df_country[interco_cols].sum(axis=1) if interco_cols else 0

        demande = df_country[prod_cols].sum(axis=1) + solde_interco

        # Calcul du prix spot horaire
        spot_prices = []
        marginal_sources = []

        for t in df_country.index:
            mix = []
            for col in prod_cols:
                source = col.split('_')[1]
                if source in cost_dict:
                    prod_value = df_country.at[t, col]
                    if prod_value > 0:
                        mix.append((cost_dict[source], source, prod_value))

            mix.sort(key=lambda x: x[0])  # tri par coût croissant

            reste = demande[t]
            prix = np.nan
            marginal = None

            for cost, source, prod in mix:
                if prod >= reste:
                    prix = cost
                    marginal = source
                    break
                else:
                    reste -= prod

            # Cas où la demande dépasse l’offre disponible
            if prix is np.nan and mix:
                prix = mix[-1][0]
                marginal = mix[-1][1]

            spot_prices.append(prix)
            marginal_sources.append(marginal)

        df[f"Estimated_Price_{country}"] = spot_prices
        df[f"marginal_tech_{country}"] = marginal_sources

    return df

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