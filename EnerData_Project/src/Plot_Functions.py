import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_timeseries(df, variables, title=None, ylabel=None, legend=True, source_type='entsoe'):
    """
    Affiche des courbes temporelles en fonction du type de source de données (entsoe, pypsa, c3s...)

    Parameters:
        df (pd.DataFrame): dataframe contenant une colonne 'DateTime' et les variables
        variables (list): liste des colonnes à afficher
        title (str): titre du graphique
        ylabel (str): nom de l'axe y
        legend (bool): affiche ou non la légende
        source_type (str): type de données ('entsoe', 'pypsa', 'c3s', etc.)
    """
    # Filtrer les lignes correspondant au type de source
    if source_type in df.columns:
        df = df[df[source_type] == source_type]

    plt.figure(figsize=(15, 5))

    for var in variables:
        if var in df.columns:
            plt.plot(df['DateTime'], df[var], label=var)

    if title:
        plt.title(f"{title} ({source_type.upper()})")
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
    """
    countries = df['country'].unique()
    price_df = pd.DataFrame(index=df['DateTime'].unique())

    for country in countries:
        df_country = df[df['country'] == country].copy()
        df_country = df_country.set_index('DateTime')

        # Récupérer toutes les colonnes de production pour ce pays
        prod_cols = [col for col in df_country.columns if col.startswith('prod_') and col.endswith(f"_{country}")]

        mix = []
        for col in prod_cols:
            source = col.split('_')[1]  # extrait NRJ_prod
            if source in cost_dict:
                mix.append((cost_dict[source], df_country[col]))

        # Créer la table triée selon le coût
        mix.sort(key=lambda x: x[0])  # trie par coût

        # Approximation de la consommation nette = somme production + solde interconnexions
        prod_total = sum([p for _, p in mix])
        interco_cols = [col for col in df_country.columns if 'interconnexion' in col.lower() and col.endswith(f"_{country}")]
        solde_interco = df_country[interco_cols].sum(axis=1) if interco_cols else 0
        demande = prod_total + solde_interco

        # Calcul du prix spot horaire
        spot_prices = []
        for t in df_country.index:
            reste = demande[t]
            prix = np.nan
            for cost, prod in mix:
                if prod[t] >= reste:
                    prix = cost
                    break
                else:
                    reste -= prod[t]
            spot_prices.append(prix)

        price_df[country] = spot_prices

    return price_df